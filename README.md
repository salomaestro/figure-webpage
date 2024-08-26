# Figure-Webpage

This is an attempt to create a simple yet reliable tool for storing and displaying figures on-the-go. It utilizes streamlit for displaying images with a local Redis database for easy injection of figures. Additionally there is a archive tool which allows for querying earlier figures.

The setup is simple and uses docker compose to setup the web and Redis containers quickly. Simply `docker compose up` begin. There is provided a test script for sending new figures.

## TODO

- [x] Implement working prototype.
- [ ] Implement simple method for sending figures, e.g., python module, shell script, etc.
- [ ] Clean up code.
