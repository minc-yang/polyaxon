---
title: "Can use Polyaxon on a custom domain?"
meta_title: "Can use Polyaxon on a custom domain? - FAQ"
meta_description: "Polyaxon ships with an ingress allowing to customize your host."
featured: false
custom_excerpt: "Polyaxon ships with an ingress allowing to customize your host."
author:
  name: "Polyaxon"
  slug: "Polyaxon"
  website: "https://polyaxon.com"
  twitter: "polyaxonAI"
  github: "polyaxon"
visibility: public
status: published
tags:
    - deployment
    - kubernetes
---

Polyaxon chart provides support for Ingress resource. You need to set `ingress.enabled` to `true` and `serviceType`  to `CluterIp` and choose an `ingress.hosts` for the URL. 
Then, you should be able to access the installation using that address.

If you want to use your own Ingress Controller such as Nginx or Traefik you maybe want to set `serviceType`  to `CluterIp` and integrate Polyaxon with your custom Ingress controller.

You can follow this steps to setup a domain:

## 1. Set up your domain
 
  1. Buy a domain name from a registrar. Pick whichever one you want.
    
  2. Create an A record from the domain you want to use, pointing to the EXTERNAL-IP of the proxy-public service. The exact way to do this will depend on the DNS provider that you’re using.
    
  3. Wait for the change to propagate. Propagation can take several minutes to several hours. Wait until you can type in the name of the domain you bought and it shows you the JupyterHub landing page.

## 2. Update your deployment config

  1. Specify your domain in the deployment config
    ```yaml
    serviceType: ClusterIp
    ingress:
      enabled: false
      hosts:
        - <your-domain-name>
    ```
   
  2. Apply the config changes by running `polyaxon deploy upgrade ...` or `helm upgrade ...`
