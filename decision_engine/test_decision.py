from decision_engine.decision_logic import decide

result = decide("201")

print("ACTION:", result["action"])
print("RISK:", result["risk"])
print("\nEXPLANATION:\n")
print(result["explanation"])
