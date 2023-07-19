"""Actions are blocks of logic that are individually processed when an Event calls
them directly, or a client sends the server a particular Command, associated with that
specific Action.

Any newly added Action classes that will be driven by Command from the client will
need to have their files created in the `cibo.actions.commands` path. Only then will
the new Action be available to clients.

Actions that are called directly by an Event (as opposed to a client Command) should
have a filename prefixed with a singular underscore.
"""
