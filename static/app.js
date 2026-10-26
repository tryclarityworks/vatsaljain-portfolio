document.querySelectorAll('[data-filter]').forEach((button) => {
  button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    let count = 0;
    document.querySelectorAll('.project[data-category]').forEach((project) => {
      project.hidden = filter !== 'all' && project.dataset.category !== filter;
      if (!project.hidden) count += 1;
    });
    document.querySelectorAll('[data-filter]').forEach((item) => {
      item.setAttribute('aria-pressed', String(item === button));
    });
    document.getElementById('project-count').textContent = `${count} project${count === 1 ? '' : 's'}`;
  });
});

document.querySelectorAll('.announce[data-until]').forEach((banner) => {
  if (Date.now() >= Date.parse(banner.dataset.until)) banner.hidden = true;
});
