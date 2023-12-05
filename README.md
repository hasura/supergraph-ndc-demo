# Installation
Clone this

Fill out the .env with your details using .env.example as a template

Run docker compose up

Navigate to http://localhost:8000/ for GraphiQL

Navigate to http://localhost:6333/ for Qdrant dashboard

## Overview

## Supergraph query

Let's see something exciting right off the bat. Not only will we query multiple data sources in a single query, but
we're also going to use a federated schema to do it. This means that we can query across multiple subgraphs, each of
which exposes a subset of the overall schema. This is a powerful concept that allows us to build a single schema that
represents our entire data model, but we can break it up into smaller pieces that are easier to manage and maintain.

Below, we're going to query across three different data sources: DuckDB, Turso, and Qdrant. Each of these data sources
is represented by a subgraph, and can be owned by different teams. We will also use Hasura's example database in our default subgraph [here](https://v3-docs-eny.pages.dev/getting-started/local-dev/)

```graphql
query SuperGraph {
  tursoArtist(limit: 5, where: { _or: [{ ArtistId: { _lt: 3 } }, { ArtistId: { _gt: 7 } }] }) {
    Albums(limit: 5) {
      AlbumId
      Tracks(limit: 5, where: { Name: { _like: "%a%" } }) {
        TrackId
        Name
      }
    }
  }
  qdrantMultimodalRecipeById(id: 1) {
    id
    name
    steps
  }
  qdrantMultimodalRecipe(args: {}, limit: 10, where: { name: { like: "%squash%" } }) {
    id
    name
    score
  }
}
```

## DuckDB - Not hosted locally

DuckDB is a high-performance, analytical database that is designed to be embedded in applications.

**You can use the DuckDB connector hosted here on Hasura DDN**:
[https://connector-e26f2620-54e3-439e-b9b1-95f873c71f50-hyc5v23h6a-ue.a.run.app](https://connector-e26f2620-54e3-439e-b9b1-95f873c71f50-hyc5v23h6a-ue.a.run.app)

### Features

- Limit
- Offset
- Ordering
- Where filtering
  - AND
  - OR
  - NOT
  - LIKE
  - GLOB
  - \>
  - <
  - \>=
  - <=
  - ==
  - !=
- Variables

### Queries

#### Example 1

```graphql
query HNDuckDB {
  duckdbSampleDataHnHackerNews(limit: 10) {
    id
    text
    time
  }
}
```

#### Example 2

```graphql
query FilteredHNNews {
  duckdbSampleDataHnHackerNews(
    limit: 10
    where: { _and: [{ title: { _like: "%tech%" } }, { _not: { text: { _like: "%apple%" } } }] }
  ) {
    id
    title
    text
    time
  }
}
```

#### Example 3

```graphql
query OrderedHNData($limitNum: Int = 5) {
  duckdbSampleDataHnHackerNews(limit: $limitNum, order_by: { time: Desc }) {
    id
    title
    text
    time
  }
}
```

## Turso - Hosted Locally, very quick

Turso is build on top of SQLite with boasted microsecond latency.

**You can use the Turso connector hosted here on Hasura DDN**:
[https://connector-de77cc89-c674-4606-bfe6-443fb20caeeb-hyc5v23h6a-ue.a.run.app](https://connector-de77cc89-c674-4606-bfe6-443fb20caeeb-hyc5v23h6a-ue.a.run.app)

### Features

- Edge-hosted
- Pagination
- Ordering
- Where filtering
  - AND
  - OR
  - NOT
  - LIKE
  - GLOB
  - \>
  - <
  - \>=
  - <=
  - ==
  - !=
- Variables
- Relationships

### Queries:

#### Example 1

```graphql
query TursoChinook {
  tursoAlbum(limit: 10, order_by: { AlbumId: Asc }, offset: 1) {
    AlbumId
    Title
    Tracks(limit: 3, order_by: { Name: Desc }) {
      TrackId
      Name
    }
  }
}
```

#### Example 2

```graphql
query AlbumsWithTracks {
  tursoAlbum(limit: 10, order_by: { Title: Asc }, where: { Title: { _glob: "*Love*" } }) {
    AlbumId
    Title
    Tracks(limit: 3, order_by: { Name: Asc }) {
      TrackId
      Name
    }
  }
}
```

## Qdrant - Hosted Locally, very quick

Qdrant is a vector search engine that allows you to search for similar vectors within embeddings.

[https://connector-47629a21-7910-4def-ae48-9ea63f297ca4-hyc5v23h6a-ue.a.run.app](https://connector-47629a21-7910-4def-ae48-9ea63f297ca4-hyc5v23h6a-ue.a.run.app)

### Features:

- Vector search with both positive and negative examples passed by ID
- Pagination
- Search scoring
- Vector search on pure vector of `Floats`
- Where filtering
  - AND
  - OR
  - NOT
  - LIKE
  - ==
  - !=
- Variables
- Remote Joins

### Queries

#### Example 1

```graphql
query RecipeRecommend($positive: [Int!] = [1]) {
  qdrantMultimodalRecipeById(id: 1) {
    id
    name
  }
  qdrantMultimodalRecipe(args: { recommend: {positive: $positive }}, limit: 10) {
    id
    name
  }
}
```

#### Example 2

```graphql
query AdvancedVectorSearch {
  positiveRecipe: qdrantMultimodalRecipeById(id: 2) {
    id
    name
  }
  negativeRecipe: qdrantMultimodalRecipeById(id: 3) {
    id
    name
  }
  qdrantMultimodalRecipe(args: { recommend: {positive: [2], negative: [3]}}, limit: 5) {
    id
    name
    score
  }
}
```


### Remote Join From Qdrant to Turso

```graphql
query QdrantJoinTurso {
  qdrantAlbum(args: {}, limit: 10) {
    id
    ArtistId
    Title
    tursoAlbum {
      AlbumId
      ArtistId
      Title
    }
    tursoArtist {
      ArtistId
      Name
    }
  }
}
```

## Typescript Function Connector

[https://connector-6606e963-47c8-4257-8563-ddb8119467be-hyc5v23h6a-ue.a.run.app](https://connector-6606e963-47c8-4257-8563-ddb8119467be-hyc5v23h6a-ue.a.run.app)

Functions:

```graphql
mutation functions {
  functionsFetchrandomdadjoke
  functionsDefineword(word: "peanut butter")
  functionsFetchcatfacts(limit: 2, max_length: 100, page: 1)
  functionsGeneraterange(start: 0, end: 3)
  functionsAddnumbers(a: 10, b: 5)
}
```

Example Output:

```json
{
  "data": {
    "functionsFetchrandomdadjoke": {
      "id": "usrcaMuszd",
      "joke": "What's the worst thing about ancient history class? The teachers tend to Babylon.",
      "status": 200
    },
    "functionsDefineword": "A spread made from ground peanuts.",
    "functionsFetchcatfacts": [
      {
        "fact": "Cats have 3 eyelids.",
        "length": 20
      },
      {
        "fact": "Cats walk on their toes.",
        "length": 24
      }
    ],
    "functionsGeneraterange": [
      0,
      1,
      2,
      3
    ],
    "functionsAddnumbers": 15
  }
}
```