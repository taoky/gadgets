# gadgets

This is a gadget collection of TaoKY.

You may see something useful or useless here.

ABSOLUTELY NO WARRANTY.

Every gadget is under Apache License unless specially claimed.

## Using sparse-checkout to clone a part of this repo

```sh
git init
git remote add -f origin git@github.com:taoky/gadgets.git
git config core.sparsecheckout true
echo "this_is_a_directory" >> .git/info/sparse-checkout # change it to the directory you want to clone
git pull origin master
```
