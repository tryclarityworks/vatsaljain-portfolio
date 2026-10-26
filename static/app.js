const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
const arrivingElements = new Set();

// Content is visible in the HTML; a short CSS entrance adds orientation.
function arrive(element) {
  if (motionPreference.matches) return;
  arrivingElements.add(element);
  element.classList.add('is-arriving');
}

document.addEventListener('animationend', (event) => {
  if (event.animationName !== 'content-arrive') return;
  event.target.classList.remove('is-arriving');
  arrivingElements.delete(event.target);
});

motionPreference.addEventListener('change', () => {
  if (!motionPreference.matches) return;
  arrivingElements.forEach((element) => element.classList.remove('is-arriving'));
  arrivingElements.clear();
});

const filters = document.querySelector('.filters');
if (filters) filters.hidden = false;
document.querySelectorAll('[data-filter]').forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    let count = 0;
    document.querySelectorAll('.project[data-category]').forEach((project) => {
      const wasHidden = project.hidden;
      project.hidden = filter !== 'all' && project.dataset.category !== filter;
      if (!project.hidden) {
        count += 1;
        if (wasHidden) arrive(project);
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
      arrive(entry.target);
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.section-heading > *, .project-main, .flow-node, .approach-grid > li, .about-photo, .about-copy > p, .video-link, .note, .contact-heading, .contact-copy').forEach((element) => observer.observe(element));
}

document.querySelectorAll('.announce[data-until]').forEach((banner) => {
  if (Date.now() >= Date.parse(banner.dataset.until)) banner.hidden = true;
});
