# one_password
python api wrapper for the 1password cli


API to wrap the 1password cli
 use the 1password entry title to query either complete 1password items or only the password
 assumes IBM as the account but can be easily modified to use any 1password account
```
 simple usage in python:

    import one_password as op
    password = op.get_password('sample')
```

## Can be run as a standalone script

Dump the entire item
```
python one_password.py --item <item to query>

```

Display the password for the item:
```
python one_password.py --password <item to query>
```
