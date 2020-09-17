This is a template for a minimalist command line script.

- README: Please always include a README file that explains the individual
  components, the customer, the project scope, login information (the actual
  passwords go into 1Password, though), etc. The more the merrier!
- main.py: Can be renamed to any reasonable file name and also duplicated. This
  is the foundation for a good command line script.

This template will allow you to pass in values for the `cluster`, `token`,
and `project_id` used by the script.

All logging is dumped to the log folder and is cleaned after 14 days.

Please adjust the path in the load.sh to the right directory for your config.sh

All three arguments are optional. If the cluster and token arguments are
present, a `SquirroClient` instance will also be created and passed into the
script for easier use.
