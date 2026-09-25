# EduGenie API Testing

The application can be tested directly from the browser or with any API client.

## Q&A

POST `/qa`

```json
{
  "text": "What is a database?"
}
```

## Explain

POST `/explain`

```json
{
  "text": "Explain inheritance in Java."
}
```

## Quiz

POST `/quiz`

```json
{
  "text": "A queue follows FIFO, meaning first in, first out.",
  "count": 3
}
```

## Summary

POST `/summarize`

```json
{
  "text": "Paste a long educational passage here."
}
```

## Learning path

POST `/learn/recommendations`

```json
{
  "text": "Python programming"
}
```

All task endpoints return:

```json
{
  "success": true,
  "result": "..."
}
```

The quiz endpoint returns an array in `result`.
