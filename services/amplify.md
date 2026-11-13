[← EC2 Image Builder](ec2-image-builder.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Elastic Beanstalk →](elastic-beanstalk.md)

# AWS Amplify (web and mobile app hosting)

**Exam domains:** [Domain 1](../01-sdlc-automation.md) | **Hands-on:** none (read-only topic)

- Build and host full-stack **web and mobile apps** (front end + managed back end such as auth, data/API, storage). Think "Elastic Beanstalk for front-end and mobile apps".
- **Amplify Hosting continuous deployment**: connect a Git repository (CodeCommit, GitHub, GitLab, Bitbucket). Each **branch** can map to its own environment (e.g., `main` -> prod, `dev` -> dev) and gets built and deployed on every push. **Pull request previews** create a temporary environment per PR.
- Build settings live in `amplify.yml` (like a buildspec). Custom domains with free managed certificates, password-protected branches, atomic deployments (new version goes live only when fully uploaded), instant rollback by redeploying a previous build.
- Exam signal: "front-end team wants Git-based CI/CD and hosting for a React/Angular/static site with minimal setup" -> Amplify Hosting.

---

[← EC2 Image Builder](ec2-image-builder.md) | [Services index](README.md) | [🏠 Home](../README.md) | [AWS Elastic Beanstalk →](elastic-beanstalk.md)
