import datetime
import json
import math
from pathlib import Path


def shop_trip() -> None:
    config_path = Path(__file__).parent / "config.json"

    with open(config_path, "r") as file:
        config = json.load(file)

        for customer in config["customers"]:
            print(f'{customer["name"]} has {customer["money"]} dollars')

            customer_x, customer_y = customer["location"]

            cheapest_shop = None
            cheapest_cost = math.inf

            for shop in config["shops"]:
                shop_x, shop_y = shop["location"]

                distance = math.sqrt(
                    (customer_x - shop_x) ** 2
                    + (customer_y - shop_y) ** 2
                )

                fuel_needed = (
                    distance
                    * customer["car"]["fuel_consumption"]
                    / 100
                )

                fuel_cost = fuel_needed * config["FUEL_PRICE"]

                products_cost = 0

                for product, amount in customer["product_cart"].items():
                    products_cost += amount * shop["products"][product]

                total_cost = fuel_cost * 2 + products_cost

                print(
                    f'{customer["name"]}\'s trip to the '
                    f'{shop["name"]} costs '
                    f"{round(total_cost, 2)}"
                )

                if total_cost < cheapest_cost:
                    cheapest_cost = total_cost
                    cheapest_shop = shop

            if customer["money"] < cheapest_cost:
                print(
                    f"{customer['name']} doesn't have enough money "
                    f"to make a purchase in any shop"
                )
                return

            print(
                f"{customer['name']} rides to "
                f"{cheapest_shop['name']}\n"
            )

            print(
                f"Date: "
                f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            )

            print(
                f"Thanks, {customer['name']}, for your purchase!"
            )

            print("You have bought:")

            total_price_of_products = 0

            for product, amount in customer["product_cart"].items():
                price = amount * cheapest_shop["products"][product]
                total_price_of_products += price

                print(
                    f"{amount} {product}s for {price:g} dollars"
                )

            print(
                f"Total cost is "
                f"{total_price_of_products} dollars"
            )

            print("See you again!\n")

            print(f"{customer['name']} rides home")

            print(
                f"{customer['name']} now has "
                f"{round(customer['money'] - cheapest_cost, 2)} dollars\n"
            )


if __name__ == "__main__":
    shop_trip()
