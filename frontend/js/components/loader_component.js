/**
 * Focus Friend - Loader Component
 * Renders a calm, steady breathing progress state to preserve ADHD focus.
 */

import { store } from '../state/store.js';

export class LoaderComponent {
  constructor() {
    this.container = document.getElementById('loader-container');
    this.statusText = document.getElementById('loader-status-text');
    this.timer = null;

    store.subscribe((state, prev) => this.render(state, prev));
    this.render(store.getState());
  }

  render(state, prev) {
    if (state.status === 'loading') {
      this.container.style.display = 'block';
      this.statusText.textContent = 'Filtering fluff & sensory noise...';

      clearTimeout(this.timer);
      this.timer = setTimeout(() => {
        if (store.getState().status === 'loading') {
          this.statusText.textContent = 'Pinpointing deadline & singular action item...';
        }
      }, 700);
    } else {
      clearTimeout(this.timer);
      this.container.style.display = 'none';
    }
  }
}
