// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Analytics helper: PostHog may be blocked or not loaded yet; never let that break the page.
function track(event, props) {
  try {
    if (window.posthog && typeof window.posthog.capture === 'function') {
      window.posthog.capture(event, props || {});
    }
  } catch (err) { /* ignore */ }
}

// Remember which page sent the visitor to /contact/ (per tab), for lead attribution.
const LEAD_SOURCE_KEY = 'lead_source_page';
function rememberSource(path) {
  try { sessionStorage.setItem(LEAD_SOURCE_KEY, path); } catch (err) { /* ignore */ }
}
function leadSourcePage() {
  try {
    const stored = sessionStorage.getItem(LEAD_SOURCE_KEY);
    if (stored) return stored;
  } catch (err) { /* ignore */ }
  try {
    if (document.referrer) {
      const ref = new URL(document.referrer);
      if (ref.origin === location.origin) return ref.pathname;
      return ref.hostname;
    }
  } catch (err) { /* ignore */ }
  return '(direct)';
}

// CTA clicks: any element with data-cta, plus every link to /contact/.
document.addEventListener('click', function (e) {
  const link = e.target.closest('a[data-cta], a[href="/contact/"], a[href="/contact"]');
  if (!link) return;
  const cta = link.getAttribute('data-cta') || 'contact-link';
  track('cta_clicked', { cta: cta, source_page: location.pathname, href: link.getAttribute('href') });
  if (location.pathname !== '/contact/') rememberSource(location.pathname);
});

// Contact form: real submission to the backend configured in _config.yml (contact_form).
const contactForm = document.getElementById('contactForm');
if (contactForm) {
  const statusBox = contactForm.querySelector('.form-status');
  const button = contactForm.querySelector('button[type="submit"]');
  const emailLink = document.querySelector('.contact-email a');
  const fallbackEmail = emailLink ? emailLink.textContent.trim() : '';
  const sourceField = contactForm.querySelector('input[name="source_page"]');
  if (sourceField) sourceField.value = leadSourcePage();

  function showStatus(kind, message) {
    if (!statusBox) return;
    statusBox.className = 'form-status form-status--' + kind;
    statusBox.textContent = message;
    statusBox.hidden = false;
  }

  function setLoading(on) {
    if (!button) return;
    button.classList.toggle('loading', on);
    button.disabled = on;
  }

  contactForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    if (!contactForm.reportValidity()) return;

    const hp = contactForm.querySelector('input[name="_gotcha"]');
    const hpBox = contactForm.querySelector('input[name="botcheck"]');
    if ((hp && hp.value) || (hpBox && hpBox.checked)) {
      // Bot filled the honeypot: act as if it worked, send nothing.
      contactForm.reset();
      showStatus('success', 'Thanks, your message was sent.');
      return;
    }

    const sourcePage = leadSourcePage();
    if (sourceField) sourceField.value = sourcePage;

    setLoading(true);
    if (statusBox) statusBox.hidden = true;

    try {
      const response = await fetch(contactForm.action, {
        method: 'POST',
        body: new FormData(contactForm),
        headers: { 'Accept': 'application/json' }
      });
      let data = {};
      try { data = await response.json(); } catch (err) { /* non-JSON answer */ }
      if (!response.ok || data.success === false) {
        throw new Error(data.message || ('HTTP ' + response.status));
      }
      contactForm.reset();
      showStatus('success', 'Thanks, your message was sent. I reply within 24 business hours.');
      track('lead_submitted', { source_page: sourcePage, form: 'contact' });
      try { sessionStorage.removeItem(LEAD_SOURCE_KEY); } catch (err) { /* ignore */ }
    } catch (err) {
      showStatus('error', 'Sorry, the message could not be sent.' +
        (fallbackEmail ? ' Please email me directly at ' + fallbackEmail + '.' : ' Please try again later.'));
      track('lead_submit_failed', { source_page: sourcePage, form: 'contact', error: String(err && err.message || err).slice(0, 200) });
    } finally {
      setLoading(false);
    }
  });
}

// Add active state to navigation links
const currentLocation = location.pathname;
const menuItems = document.querySelectorAll('.nav-link');
menuItems.forEach(item => {
  if(item.getAttribute('href') === currentLocation){
    item.classList.add('active');
  }
});

// Header background on scroll and hide/show on scroll direction
let lastScrollTop = 0;
const header = document.querySelector('.site-header');
if (header) {
  window.addEventListener('scroll', function() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    // Background opacity
    if (scrollTop > 100) {
      header.style.background = 'rgba(10, 25, 47, 0.98)';
    } else {
      header.style.background = 'rgba(10, 25, 47, 0.95)';
    }
    // Hide/show on scroll direction
    if (scrollTop > lastScrollTop && scrollTop > 100) {
      // Scrolling down
      header.classList.add('header-hidden');
    } else {
      // Scrolling up
      header.classList.remove('header-hidden');
    }
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For Mobile or negative scrolling
  });
}
