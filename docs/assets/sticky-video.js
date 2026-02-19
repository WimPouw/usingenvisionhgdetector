<script>
(function () {
  const widget = document.querySelector('.video-widget');
  if (!widget) return;

  // --- Collapse toggle ---
  const btn = document.createElement('button');
  btn.className = 'video-toggle-btn';
  btn.textContent = '−';
  widget.appendChild(btn);

  btn.addEventListener('click', () => {
    widget.classList.toggle('collapsed');
    btn.textContent = widget.classList.contains('collapsed') ? '+' : '−';
  });

  // --- Keep widget within viewport height on scroll ---
  const MARGIN_TOP = 80;    // px from top of viewport
  const MARGIN_BOTTOM = 20; // px from bottom of viewport

  function clampPosition() {
    const vh = window.innerHeight;
    const widgetH = widget.offsetHeight;
    const maxTop = vh - widgetH - MARGIN_BOTTOM;
    const clampedTop = Math.min(MARGIN_TOP, maxTop);
    widget.style.top = clampedTop + 'px';
  }

  window.addEventListener('scroll', clampPosition, { passive: true });
  window.addEventListener('resize', clampPosition);
  clampPosition();
})();
</script>