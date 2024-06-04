import requests

# Function to fetch recipes based on user input
def fetch_recipes(food_category, from_index):
    # Replace 'YOUR_APP_ID' and 'YOUR_API_KEY' with your actual Edamam API credentials
    app_id = 'API-ID'
    api_key = 'API-KEY'
    base_url = 'https://api.edamam.com/search'
    params = {
        'q': food_category,
        'app_id': app_id,
        'app_key': api_key,
        'from': from_index,
        'to': from_index + 10  # Number of recipes to fetch (adjust as needed)
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data['hits']
    else:
        return None

# Function to fetch nutritional information for a specific ingredient
def fetch_nutritional_info(ingredient_name):
    # Replace 'YOUR_APP_ID' and 'YOUR_API_KEY' with your actual Edamam API credentials
    app_id = '6caff4e6'
    api_key = '8b9a7c2ed9ad88d54e8ae13b88bbf7a3'
    base_url = 'https://api.edamam.com/api/food-database/v2/parser'
    params = {
        'ingr': ingredient_name,
        'app_id': app_id,
        'app_key': api_key
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'hints' in data and data['hints']:
            return data['hints'][0]['food']['nutrients']
        else:
            return None
    else:
        return None

# Function to display recipe details
def display_recipe_details(recipe):
    print(f"\nRecipe: {recipe['recipe']['label']}")
    print("Ingredients:")
    for i, ingredient in enumerate(recipe['recipe']['ingredientLines'], start=1):
        print(f"{i}. {ingredient}")
    print("Cooking Method:")
    print(recipe['recipe']['url'])

# Function to display nutritional information for an ingredient
def display_nutritional_info(ingredient_name, nutritional_info):
    print(f"\nNutritional Information for {ingredient_name}:")
    print("Calories:", nutritional_info.get('ENERC_KCAL', 'N/A'))
    print("Protein:", nutritional_info.get('PROCNT', 'N/A'))
    print("Fat:", nutritional_info.get('FAT', 'N/A'))
    print("Carbohydrates:", nutritional_info.get('CHOCDF', 'N/A'))

# Main function
def main():
    print("Welcome to Recipe Recommendation Chatbot!\n")

    # User input for food category
    food_category = input("Select a food category (e.g., chicken, pasta, salad): ")

    from_index = 0

    while True:
        # Fetch recipes based on user input
        recipes = fetch_recipes(food_category, from_index)

        if recipes:
            # Display recipe list
            print("\nAvailable Recipes:")
            for i, recipe in enumerate(recipes, start=1):
                print(f"{i}. {recipe['recipe']['label']}")

            # User input for recipe selection
            selected_recipe_index = int(input("\nEnter the number corresponding to the recipe you'd like to explore (0 to choose a new category, -1 to exit): "))

            if selected_recipe_index == -1:
                print("Thank you for using Recipe Recommendation Chatbot. Goodbye!")
                break

            if selected_recipe_index == 0:
                # User wants to choose a new category
                food_category = input("Select a new food category: ")
                from_index = 0  # Reset from_index
                continue

            selected_recipe = recipes[selected_recipe_index - 1]

            # Display recipe details
            print("\nRecipe Details:")
            display_recipe_details(selected_recipe)

            # User input for checking if found the desired dish
            found_dish = input("\nDid you find the dish you were looking for? (yes/no): ")

            if found_dish.lower() == 'yes':
                # User found the dish
                print("Enjoy cooking!")
                break
            else:
                # User didn't find the dish
                dish_number = input("Enter the dish number from the list or type 'no' to see more recipes: ")
                if dish_number.lower() == 'no':
                    from_index += 10
                else:
                    try:
                        selected_recipe_index = int(dish_number)
                        selected_recipe = recipes[selected_recipe_index - 1]
                        display_recipe_details(selected_recipe)
                    except ValueError:
                        print("Invalid input. Please enter a valid dish number or 'no' to see more recipes.")

        else:
            print("\nError fetching recipes. Please try again later.")
            break

if __name__ == "__main__":
    main()
