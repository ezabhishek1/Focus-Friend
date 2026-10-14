/**
 * Focus Friend - Frontend Application Entrypoint
 * Bootstraps modular UI components, reactive store, and API service with error boundaries.
 */

import { HeaderComponent } from './components/header_component.js';
import { PresetsComponent } from './components/presets_component.js';
import { InputComponent } from './components/input_component.js';
import { OutputComponent } from './components/output_component.js';
import { LoaderComponent } from './components/loader_component.js';
import { ModalComponent } from './components/modal_component.js';
import { store } from './state/store.js';
import { ApiService } from './services/api_service.js';

class App {
  async init() {
    try {
      // 1. Initialize modular UI components
      new HeaderComponent();
      new PresetsComponent();
      new InputComponent();
      new OutputComponent();
      new LoaderComponent();
      new ModalComponent();

      // 2. Fetch overwhelm presets from backend with graceful fallback
      try {
        const presets = await ApiService.fetchPresets();
        store.setPresets(presets);
      } catch (err) {
        console.debug('[App] Presets loaded from static fallback:', err);
      }

      // 3. Check backend health & local Ollama daemon status
      await store.checkSystemHealth();

      console.log("⚡ Focus Friend application initialized successfully.");
    } catch (fatalErr) {
      console.error("[App] Fatal UI initialization error:", fatalErr);
    }
  }
}

window.addEventListener('DOMContentLoaded', () => {
  const app = new App();
  app.init();
});
