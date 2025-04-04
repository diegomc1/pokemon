from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Pokemon API",
    description="A simple API to fetch Pokemon data from PokeAPI",
    version="1.0.0"
)

# Setup CORS Cross-Origin Resource Sharing
# Allows all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PokemonResponse(BaseModel):
    id: int
    name: str
    height: int
    weight: int
    abilities: list[str]
    types: list[str]
    base_experience: int
    sprite_url: Optional[str] = None
    moves: list[str]

async def fetch_pokemon_data(identifier: str | int) -> dict:
    """
    Get Pokemon information by ID or name
    
    Parameters:
    - identifier: Pokemon's ID (number) or name (string)
    
    Returns:
    - Pokemon information including ID, name, height, weight, abilities, types, etc.
    """
    url = f"https://pokeapi.co/api/v2/pokemon/{identifier}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        # Catch error 404 not found
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=404,
                detail=f"Pokemon with identifier '{identifier}' not found"
            )
        # Catch error 503 service unavailable
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail="Unable to connect to PokeAPI"
            )

def transform_pokemon_data(raw_data: dict) -> PokemonResponse:
    """
    Transform the raw PokeAPI data into our response model
    """
    return PokemonResponse(
        id=raw_data["id"],
        name=raw_data["name"],
        height=raw_data["height"],
        weight=raw_data["weight"],
        abilities=[ability["ability"]["name"] for ability in raw_data["abilities"]],
        types=[type_data["type"]["name"] for type_data in raw_data["types"]],
        base_experience=raw_data["base_experience"],
        sprite_url=raw_data["sprites"]["front_default"],
        moves= [move["move"]["name"] for move in raw_data["moves"]]
    )

@app.get("/pokemon/{identifier}", response_model=PokemonResponse)
async def get_pokemon(identifier: str | int):
    raw_data = await fetch_pokemon_data(identifier)
    return transform_pokemon_data(raw_data)

@app.get("/")
async def root():
    return {"message": "Pokemon API is running"}