# fast-api




-- Need to add a user product middleware -- does the user have access to this product then create indexes for the userproduct access indexes
-- 


Links:
-- https://httpie.io/app


Notes:
-- The application would connect to MongoDB using a connection string that is passed in an environment variable.

There are actually two Python drivers for MongoDB — 
PyMongo and Motor — but only one of them is suitable for use with FastAPI. Because FastAPI is built on top of  ASGI and asyncio
,you need to use Motor, which is compatible with asyncio. PyMongo is only for synchronous applications. Fortunately, just like PyMongo, Motor is developed and fully supported by MongoDB, so you can rely on it in production, just like you would with PyMongo.


https://www.mongodb.com/developer/products/mongodb/8-fastapi-mongodb-best-practices/


This is to make sure on startup the database is initialised and connected

``` from contextlib import asynccontextmanager
from logging import info @asynccontextmanager
async def db_lifespan(app: FastAPI):
    # Startup
    app.mongodb_client = AsyncIOMotorClient(CONNECTION_STRING)
    app.database = app.mongodb_client.get_default_database()
    ping_response = await app.database.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        info("Connected to database cluster.")
    
    yield

    # Shutdown
    app.mongodb_client.close()


app: FastAPI = FastAPI(lifespan=db_lifespan) ```



a Pydantic-based ODM, such as ODMantic or Beanie - odmantic, an ODM library built on top of motor for MongoDB, allowing Python objects to map to MongoDB documents.

The reason you should prefer one of these libraries is that FastAPI is built with tight integration to Pydantic. This means that if your path operations return a Pydantic object, the schema will automatically be documented using OpenAPI (which used to be called Swagger), and FastAPI also provides nice API documentation under the path "/docs".


class Profile(Document):
    """
    A profile for a single user as a Beanie Document.

    Contains some useful information about a person.
    """

    # Use a string for _id, instead of ObjectID:
    id: Optional[str] = Field(default=None, description="MongoDB document ObjectID")
    username: str
    birthdate: datetime
    website: List[str]

    class Settings:
        # The name of the collection to store these objects.
        name = "profiles"

# A sample path operation to get a Profile:
@app.get("/profiles/{profile_id}")
async def get_profile(profile_id: str) -> Profile:
    """
    Look up a single profile by ID.
    """
    # This API endpoint demonstrates using Motor directly to look up a single
    # profile by ID.
    profile = await Profile.get(profile_id)
    if profile is not None:
        return profile
    else:
        raise HTTPException(
            status_code=404, detail=f"No profile with id '{profile_id}'"
        )

Create indexes on frequently queried fields

It's possible to customize the collection name of a model by specifying the collection option in the model_config class attribute.
