/**
 * Focus Friend - API Client Service
 * Handles communication with backend REST API v1 with automatic fallback & error handling.
 */

import { CONFIG } from '../config.js';
import { LocalHeuristicEngine } from './local_engine.js';

/**
 * Creates an AbortSignal with timeout, safely falling back for older browser runtimes.
 * @param {number} ms - Milliseconds before timeout.
 * @returns {AbortSignal}
 */
function createTimeoutSignal(ms) {
  if (typeof AbortSignal !== 'undefined' && typeof AbortSignal.timeout === 'function') {
    return AbortSignal.timeout(ms);
  }
  const controller = new AbortController();
  setTimeout(() => controller.abort(), ms);
  return controller.signal;
}

export class ApiService {
  /**
   * Health and Ollama daemon connectivity check.
   * @returns {Promise<{ollama_connected: boolean, active_model: string|null, status: string}>}
   */
  static async checkHealth() {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/health`, {
        method: 'GET',
        headers: { 'Accept': 'application/json' },
        signal: createTimeoutSignal(3500),
      });

      if (!response.ok) {
        throw new Error(`Health check returned status ${response.status}`);
      }
      return await response.json();
    } catch (err) {
      console.warn('[ApiService] Backend health check failed, using offline heuristics mode:', err.message);
      return {
        ollama_connected: false,
        active_model: null,
        status: 'offline_fallback',
        fallback_engine_available: true,
      };
    }
  }

  /**
   * Fetches presets from backend, falling back to static default presets.
   * @returns {Promise<Array>}
   */
  static async fetchPresets() {
    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/presets`, {
        method: 'GET',
        headers: { 'Accept': 'application/json' },
        signal: createTimeoutSignal(3000),
      });

      if (response.ok) {
        const data = await response.json();
        return data.presets || CONFIG.DEFAULT_PRESETS;
      }
    } catch (err) {
      console.debug('[ApiService] Presets endpoint unavailable, using static defaults:', err.message);
    }
    return CONFIG.DEFAULT_PRESETS;
  }

  /**
   * Distills raw unstructured message text into Tone, Timeline, and Task.
   * Falls back to client-side LocalHeuristicEngine on any network failure.
   * 
   * @param {string} text - Raw message input.
   * @param {string|null} [model=null] - Optional model override.
   * @returns {Promise<Object>} Distilled signal response.
   */
  static async extract(text, model = null) {
    const cleanText = (text || '').trim();
    if (cleanText.length < 5) {
      throw new Error("Please enter at least 5 characters to extract signal.");
    }

    try {
      const response = await fetch(`${CONFIG.API_BASE_URL}/extract`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ text: cleanText, model }),
        signal: createTimeoutSignal(CONFIG.TIMEOUT_MS),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const message = errorData.detail || errorData.error || `Server responded with ${response.status}`;
        throw new Error(message);
      }

      return await response.json();
    } catch (apiError) {
      console.warn('[ApiService] Backend API request failed. Activating Zero-Cloud client fallback:', apiError.message);
      // Client-side fallback guarantees 100% offline uptime with zero data leaks
      return LocalHeuristicEngine.distill(cleanText);
    }
  }
}
