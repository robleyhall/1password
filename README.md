# 1password
python api wrapper for the 1password cli


API to wrap the 1password cli

use the 1password entry `title` to query either complete 1password items or only the password
assumes `IBM` as the account but can be easily modified to use any 1password account.
 
The module caches the session token to prevent repeated password prompts as long as the token remains valid. 1Password documentation says tokens expire after 30 mins of inactivity.
## Basic python library use

```
    import one_password as op
    password = op.get_password('sample')
```

## Can be run as a standalone script

Dump an entire item
```
python one_password.py --item <item to query>
```

Display the password for the item:
```
python one_password.py --password <item to query>
```
