To deploy this connector, run the following command in the functions/src directory.

```
hasura3 connector create functions:v1 \ 
  --github-repo-url https://github.com/hasura/ndc-typescript-deno/tree/main \
  --config-file <(echo '{}') \
  --volume ./functions:/functions
```

