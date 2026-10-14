/**
 * Focus Friend - Modal Component
 * Controls the Manifesto, PRD story, and keyboard shortcuts modal.
 */

import { audioService } from '../services/audio_service.js';

export class ModalComponent {
  constructor() {
    this.modal = document.getElementById('modal-manifesto');
    this.btnOpen = document.getElementById('btn-open-manifesto');
    this.btnClose = document.getElementById('btn-close-modal');
    this.btnCloseBottom = document.getElementById('btn-close-modal-bottom');

    this.bindEvents();
  }

  bindEvents() {
    if (this.btnOpen) {
      this.btnOpen.addEventListener('click', () => {
        audioService.play('click');
        this.open();
      });
    }

    if (this.btnClose) {
      this.btnClose.addEventListener('click', () => this.close());
    }

    if (this.btnCloseBottom) {
      this.btnCloseBottom.addEventListener('click', () => this.close());
    }

    if (this.modal) {
      this.modal.addEventListener('click', (e) => {
        if (e.target === this.modal) this.close();
      });
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && this.modal && this.modal.style.display !== 'none') {
        this.close();
      }
    });
  }

  open() {
    if (this.modal) this.modal.style.display = 'flex';
  }

  close() {
    if (this.modal) this.modal.style.display = 'none';
  }
}
