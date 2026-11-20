---
layout: default
title: Contact
permalink: /contact/
---

<section class="contact-hero section--full">
  <div class="inner">
    <div class="footer-content">
      <div class="contact-section">
        <h1 class="contact-title">Get in Touch</h1>
        <p>Ready to discuss your project? Let's connect and explore how I can help achieve your technical goals.</p>
        {%- assign cf = site.contact_form -%}
        {%- if cf.action and cf.action != "" %}
        <form id="contactForm" class="contact-form" action="{{ cf.action }}" method="POST" accept-charset="UTF-8">
          <input type="hidden" name="source_page" value="">
          <div class="form-hp" aria-hidden="true">
            <label for="website">Leave this field empty</label>
            <input type="text" id="website" name="_gotcha" tabindex="-1" autocomplete="off">
            <input type="checkbox" name="botcheck" tabindex="-1" autocomplete="off">
          </div>
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" id="name" name="name" autocomplete="name" required>
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" name="email" autocomplete="email" required>
          </div>
          <div class="form-group">
            <label for="project">Project Details</label>
            <textarea id="project" name="message" rows="4" placeholder="Brief description of your project requirements, timeline, and budget range" required></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Send Inquiry</button>
          <div class="form-status" role="status" aria-live="polite" hidden></div>
        </form>
        {%- endif %}
        <p class="contact-email">Prefer email? Write to <a href="mailto:{{ site.email }}" data-cta="contact-mailto">{{ site.email }}</a>.</p>
      </div>
      <div class="info-section">
        <h3>Professional Info</h3>
        <div class="info-grid">
          <div class="info-item">
            <strong>Location:</strong>
            <span>Bucharest, Romania</span>
          </div>
          <div class="info-item">
            <strong>Availability:</strong>
            <span>20+ hours/week</span>
          </div>
          <div class="info-item">
            <strong>Response Time:</strong>
            <span>24 business hours</span>
          </div>
          <div class="info-item">
            <strong>Preferred Projects:</strong>
            <span>1-6 months</span>
          </div>
        </div>
        <div class="social-links">
          <a href="https://github.com/ciuc123" target="_blank" class="social-link">
            <i class="fab fa-github"></i>
            <span>GitHub</span>
          </a>
          <a href="https://www.linkedin.com/in/andrei-ciuculescu/" target="_blank" class="social-link">
            <i class="fab fa-linkedin"></i>
            <span>LinkedIn</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</section>
