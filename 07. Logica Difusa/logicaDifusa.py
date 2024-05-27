import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

age = ctrl.Antecedent(np.arange(0, 21, 1), 'age')
preferred_duration = ctrl.Antecedent(
    np.arange(0, 121, 1), 'preferred_duration')
favorite_genre = ctrl.Antecedent(np.arange(0, 11, 1), 'favorite_genre')

recommendation_quality = ctrl.Consequent(
    np.arange(0, 11, 1), 'recommendation_quality')
recommendation_duration = ctrl.Consequent(
    np.arange(0, 11, 1), 'recommendation_duration')
recommendation_genre_match = ctrl.Consequent(
    np.arange(0, 11, 1), 'recommendation_genre_match')

age['child'] = fuzz.trimf(age.universe, [0, 0, 10])
age['preteen'] = fuzz.trimf(age.universe, [7, 12, 15])
age['teen'] = fuzz.trimf(age.universe, [13, 20, 20])

preferred_duration['short'] = fuzz.trimf(
    preferred_duration.universe, [0, 0, 60])
preferred_duration['medium'] = fuzz.trimf(
    preferred_duration.universe, [30, 60, 90])
preferred_duration['long'] = fuzz.trimf(
    preferred_duration.universe, [60, 120, 120])

favorite_genre['adventure'] = fuzz.trimf(favorite_genre.universe, [0, 0, 3])
favorite_genre['comedy'] = fuzz.trimf(favorite_genre.universe, [2, 5, 7])
favorite_genre['educational'] = fuzz.trimf(
    favorite_genre.universe, [6, 10, 10])

recommendation_quality['low'] = fuzz.trimf(
    recommendation_quality.universe, [0, 0, 5])
recommendation_quality['medium'] = fuzz.trimf(
    recommendation_quality.universe, [2, 5, 8])
recommendation_quality['high'] = fuzz.trimf(
    recommendation_quality.universe, [5, 10, 10])

recommendation_duration['short'] = fuzz.trimf(
    recommendation_duration.universe, [0, 0, 5])
recommendation_duration['medium'] = fuzz.trimf(
    recommendation_duration.universe, [2, 5, 8])
recommendation_duration['long'] = fuzz.trimf(
    recommendation_duration.universe, [5, 10, 10])

recommendation_genre_match['low'] = fuzz.trimf(
    recommendation_genre_match.universe, [0, 0, 5])
recommendation_genre_match['medium'] = fuzz.trimf(
    recommendation_genre_match.universe, [2, 5, 8])
recommendation_genre_match['high'] = fuzz.trimf(
    recommendation_genre_match.universe, [5, 10, 10])

rules = [
    ctrl.Rule(age['child'] & preferred_duration['short'] & favorite_genre['adventure'],
              (recommendation_quality['high'], recommendation_duration['short'], recommendation_genre_match['high'])),
    ctrl.Rule(age['child'] & preferred_duration['short'] & favorite_genre['comedy'],
              (recommendation_quality['high'], recommendation_duration['short'], recommendation_genre_match['high'])),
    ctrl.Rule(age['child'] & preferred_duration['short'] & favorite_genre['educational'],
              (recommendation_quality['high'], recommendation_duration['short'], recommendation_genre_match['high'])),
    ctrl.Rule(age['preteen'] & preferred_duration['medium'] & favorite_genre['adventure'],
              (recommendation_quality['high'], recommendation_duration['medium'], recommendation_genre_match['high'])),
    ctrl.Rule(age['preteen'] & preferred_duration['medium'] & favorite_genre['comedy'],
              (recommendation_quality['medium'], recommendation_duration['medium'], recommendation_genre_match['medium'])),
    ctrl.Rule(age['preteen'] & preferred_duration['medium'] & favorite_genre['educational'],
              (recommendation_quality['high'], recommendation_duration['medium'], recommendation_genre_match['high'])),
    ctrl.Rule(age['teen'] & preferred_duration['long'] & favorite_genre['adventure'],
              (recommendation_quality['medium'], recommendation_duration['long'], recommendation_genre_match['medium'])),
    ctrl.Rule(age['teen'] & preferred_duration['long'] & favorite_genre['comedy'],
              (recommendation_quality['medium'], recommendation_duration['long'], recommendation_genre_match['medium'])),
    ctrl.Rule(age['teen'] & preferred_duration['long'] & favorite_genre['educational'],
              (recommendation_quality['high'], recommendation_duration['long'], recommendation_genre_match['high'])),
    ctrl.Rule(age['teen'] & preferred_duration['short'] & favorite_genre['adventure'],
              (recommendation_quality['medium'], recommendation_duration['short'], recommendation_genre_match['medium'])),
]

control_system = ctrl.ControlSystem(rules)
simulation = ctrl.ControlSystemSimulation(control_system)

simulation.input['age'] = 10
simulation.input['preferred_duration'] = 50
simulation.input['favorite_genre'] = 4

simulation.compute()

quality = simulation.output['recommendation_quality']
duration = simulation.output['recommendation_duration']
genre_match = simulation.output['recommendation_genre_match']

print(f"Recommendation Quality: {quality}")
print(f"Recommendation Duration: {duration}")
print(f"Recommendation Genre Match: {genre_match}")

if quality >= 7 and duration >= 7 and genre_match >= 7:
    print("Recommended Movies/Series: 'Toy Story', 'Zootopia', 'Coco', 'Moana', 'Tangled'")
elif quality >= 5 and duration >= 5 and genre_match >= 5:
    print("Recommended Movies/Series: 'Frozen', 'The Incredibles', 'Finding Nemo', 'Big Hero 6', 'Despicable Me'")
else:
    print("Recommended Movies/Series: 'Peppa Pig', 'Dora the Explorer', 'Bluey', 'Paw Patrol', 'My Little Pony'")

recommendation_quality.view(sim=simulation)
recommendation_duration.view(sim=simulation)
recommendation_genre_match.view(sim=simulation)
