```
kubeq -s [app]=thing
```

gives pretty table of everythig with that label

```
https://kubernetes.io/docs/concepts/cluster-administration/flow-control/

kubeq [app=thing] -- EXEC
kubeq [app=thing] -- PORT-FORWARD
kubeq [app=thing] -- PAUSE
kubeq [app=thing] -- RESUME
kubeq Deploy[app=thing] --> Pod -- DELETE
kubeq -k Deploy -s [app=thing] --> Pod -- DELETE


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
