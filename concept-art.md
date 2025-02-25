```
kubeq -s [app]=thing
```

gives pretty table of everythig with that label

```
kubeq -s [app]=thing
kubeq -s ns=thing
kubeq --selector='ns=thing [app] in (1, 2)'

```

```bash
kubeq \
    -w 'kind=pod' \
    -w '[app]=thing' \
    --where 'ns=thing' '[app] in (1, 2)' \
    --map 'kind=dep' '%ident in (status.pods)'
```

Results in:

```
Running commands:
* delete thing1 -n thing
* delete thing2 -n thing
* delete thing3 -n thing
```
