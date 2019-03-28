# XploiteD

 A Flask web application with several vulnerabilities to be exploited.


### Prerequisites

- Docker (& Docker compose)
- Python 3.6


### App setup & run
```bash
$ docker-compose build
$ docker-compose up
```

### Existing weaknesses

|CWE ID | CWE Name |
|----------------------------|-----------------------------|
|CWE-79 | Improper Neutralization of Input During Web Page Generation (XSS)|
|CWE-97| Improper Neutralization of Server-Side Includes (SSI) Within a Web Page|
|CWE-209| Information Exposure Through an Error Message|
|CWE-307| Improper Restriction of Excessive Authentication Attempts|
|CWE-331| Insufficent Entropy|
|CWE-346| Origin Validation Error |
|CWE-352| Cross-Site Request Forgery|
|CWE-451| UI Misrepresentation of Critical Information|
|CWE-614| Sensitive Cookie in HTTPS Session Without 'Secure' Attribute|
|CWE-799| Improper Control Of Interaction Frequency|
|CWE-837| Improper Enforcement of Single, Unique Action|
|CWE-841| Improper Enforcement Of Behavioral Workflow|
|CWE-1021| Improper Restriction of UI layers or frames|
