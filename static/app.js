const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
const arrivingElements = new Set();

// Content is visible in the HTML; a short CSS entrance adds orientation.
function arrive(element, delay = 0) {
  if (motionPreference.matches) return;
  arrivingElements.add(element);
  element.style.animationDelay = `${delay}ms`;
  element.classList.add('is-arriving');
}

document.addEventListener('animationend', (event) => {
  if (!['content-arrive', 'handoff-arrive'].includes(event.animationName)) return;
  event.target.classList.remove('is-arriving');
  event.target.style.removeProperty('animation-delay');
  arrivingElements.delete(event.target);
});

motionPreference.addEventListener('change', () => {
  if (!motionPreference.matches) return;
  arrivingElements.forEach((element) => {
    element.classList.remove('is-arriving');
    element.style.removeProperty('animation-delay');
  });
  arrivingElements.clear();
});

const filters = document.querySelector('.filters');
if (filters) filters.hidden = false;
document.querySelectorAll('[data-filter]').forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    document.querySelector('.project-list').dataset.filtered = String(filter !== 'all');
    let count = 0;
    document.querySelectorAll('.project[data-category]').forEach((project) => {
      project.hidden = filter !== 'all' && project.dataset.category !== filter;
      if (!project.hidden) {
        count += 1;
      }
    });
    document.querySelectorAll('[data-filter]').forEach((item) => {
      item.setAttribute('aria-pressed', String(item === button));
    });
    document.getElementById('project-count').textContent = `${count} project${count === 1 ? '' : 's'}`;
  });
});

if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.querySelectorAll('[data-reveal]').forEach((step, index) => arrive(step, index * 70));
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.artifact').forEach((element) => observer.observe(element));
}

document.querySelectorAll('.announce[data-until]').forEach((banner) => {
  if (Date.now() >= Date.parse(banner.dataset.until)) banner.hidden = true;
});
