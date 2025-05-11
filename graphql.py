# backend/routes/graphql.py

from fastapi import APIRouter
from ariadne import QueryType, make_executable_schema, graphql
from ariadne.asgi import GraphQL

# Define GraphQL schema
type_defs = """
  type Product {
    id: ID!
    name: String!
    price: Float!
    image_url: String
  }

  type Query {
    recommendations(userId: ID!): [Product!]!
  }
"""

query = QueryType()

@query.field("recommendations")
def resolve_recommendations(_, info, userId):
    from services.recommendation_engine import recommend_products
    # returns list of product names; adapt to full product objects in real usage
    products = recommend_products(int(userId))
    return [{"id": p.id, "name": p.name, "price": p.price, "image_url": p.image_url} for p in products]

schema = make_executable_schema(type_defs, query)
graphql_app = GraphQL(schema, debug=True)

router = APIRouter()
router.add_route("/graphql", graphql_app)
router.add_websocket_route("/graphql", graphql_app)
