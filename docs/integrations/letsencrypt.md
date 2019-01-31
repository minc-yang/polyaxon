---
title: "Let's Encrypt"
meta_description: "Ensure your Polyaxon deployment is secure with a free SSL certificate via a full integration with Let's Encrypt."
custom_excerpt: "Making the web more secure with free SSL certificates, Let's Encrypt is a great way to make your Polyaxon deployment run on HTTPS"
image: "../../content/images/integrations/letsencrypt.png"
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
tags: 
  - security
featured: true
visibility: public
status: published
---

We strongly recommend that you use SSL for your Polyaxon deployment.


## Polyaxon PaaS

All **Polyaxon PaaS** come with automatic SSL enabled by default and require no setup of any kind.


## Self-Hosting

If you use our Polyaxon CE or Polyaxon EE hosted on your cluster; you will need to Configure an SSL yourself.

Let's Encrypt allows you to provision a new SSL certificate.

>**N.B.**: You can, of course, only setup SSL if you have a properly configured domain name. Let's Encrypt will not be able to provision a certificate for any Polyaxon deployment which is running locally, or on an IP address.
