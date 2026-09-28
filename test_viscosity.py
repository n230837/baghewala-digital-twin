from src.viscosity_model import viscosity_arrhenius


temperatures = [40, 45, 50, 55, 60, 70, 80, 100]

print("Baghewala Heavy-Oil Viscosity")
print("-----------------------------")

for temperature in temperatures:
    viscosity = viscosity_arrhenius(temperature)

    print(
        f"{temperature} °C → {viscosity:.2f} cP"
    )