# XploiteD

 A Flask web application with several vulnerabilities to be exploited.

![xploited_app_screenshot](https://uc864af7fdf258a80ca948f7cb19.previews.dropboxusercontent.com/p/thumb/AAZSYpVZlDrP5r0mXtyQDJekP-KIdYgJTGIU8-Cy4HYTt3GGXE_slY37bV2e_b--noUY506uc0_5194o8RXulz-c_vK0C__sjIAVg9_b0AdeCA_92JHbmBXrNLwWwAHYYjwCuZGlaCvucH__eQhTG5Smo3P-zyIfLOQeBDimiu4G6EUB-SjA34URAxWjBwRCbSu5d7krw6dz5t8PSAhPtgrdXfVX-XiWGZXn9ugpq5da8I-jtw14P6D4QRhJT2B_nWNYvwR6BNUPX_AQQx98X-coNPlTm2qdgp6DJBW4G43rI49ouffXzKEaRpPzGhwyX5-9Y2wZa7bhnmHxIBGS7-S_AbS69nGZ5RhUw2W2EADhyV5fQxDPHLgjzmz3a4EkH5FM9K1d8tMcCoWvgqDNzVp8rExUUW5FFo4zwWisqWYlfIgM60FJo7qUPbYv9MeOJcQ/p.png)

### Existing weaknesses

|CWE ID | CWE Name |
|----------------------------|-----------------------------|
|CWE-79 | Improper Neutralization of Input During Web Page Generation (XSS)|
|CWE-97| Improper Neutralization of Server-Side Includes (SSI) Within a Web Page|
|CWE-209| Information Exposure Through an Error Message|
|CWE-307| Improper Restriction of Excessive Authentication Attempts|
|CWE-331| Insufficent Entropy|
|CWE-352| Cross-Site Request Forgery|
|CWE-451| UI Misrepresentation of Critical Information|
|CWE-614| Sensitive Cookie in HTTPS Session Without 'Secure' Attribute|
|CWE-799| Improper Control Of Interaction Frequency|
|CWE-837| Improper Enforcement of Single, Unique Action|
|CWE-841| Improper Enforcement Of Behavioral Workflow|
|CWE-1021| Improper Restriction of UI layers or frames|


### App setup & run
```bash
$ docker build -t xploited .; docker run -it -p 5000:5000 xploited
```
