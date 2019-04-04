class FormError(BaseException):
    def __init__(this, msg):
        this.msg = msg

def get_avail_choices(choicepath):
    return choices[choicepath]

choices = {'0':[None,
                """You are sitting at the base of a mountain with a stick by your feet.
At the top of the mountain sits a menacing fortress guarded by undead.
To your right is an abandoned shack, dilapidated from years of weather.
In front of you are giant stone steps leading up the mountain.""",
                None,
                1,2,3],
            '01':["Pick up stick",
                     "stick",
                     None],
            '02':["Go to house",
                     """Inside of the house you find a haggard sorcerer prying
at a door on the wall. There is a small slit between the door and the wall.
The sorcerer notices you standing and beckons to you.""",
                     None,
                     1,2],
            '03':["Go up mountain",
                     """You trudge up the mountain steps, walking until you
reach a small clearing where there stands a single apple tree. At the base
of the tree is a pool of water that is eerily reflective. You are very thirsty
from the walk.""",
                     None,
                     1,2],
           '031':["Investigate the apple tree",
                  "apple",
                  None],
           '032':["Go to take a drink from the pool",
                  """You walk over to the pool, dropping to your knees and
bending over to drink the water. As you lower your head to drink, you see
bones lying at the bottom of the pool and pause.""",
                  None,
                  1,2,3],
           '0321':["Drink the water anyways",
                   """You take a deep sip of the water and instantly you can
feel your stomach start twisting and turning in agony. You died of dysentery."""],
           '0322':["Try to grab the bones from the bottom of the pool",
                   """You reach down and grasp for the bones. As soon as you
touch the bones they snap into action! The undead arm flails, attempting to
pull you down and drown you.""",
                   None,
                   1,2],
           '0323':["Wait and examine the surface of the water",
                   """As you stare at the water closer the surface starts to
coalesce, gaining a mirror-like sheen. The surface starts to shift and you see
fire and smoke.""",
                   None,
                   1,2],
           '03231':["Enter the portal",
                    """YOU WON""",
                    None],
           '03232':["Get up and continue up the mountain",
                    """You stand and cast your gaze back up the rocky mountain
path. Around the next rim you see what looks to be smoke rising and wooden
spikes.""",
                    None]
           '03221':["Use your stick to bludgeon the arm",
                    """You grasp the stick from the ground where you laid it,
swinging at the skeleton. With a resounding thud, the arm falls to pieces and
you are free.(adding more to this path)""",
                    "stick",
                    1,2],
           '03222':["TODO:DESC",
                    """TODO:SIT""",
                    None,
                    1,2],
            '021':["Talk to the sorcerer",
                      """\'Ah yes an adventurer. Could you possibly help me
open this door? I can promise you a reward...\' the man croaks. He looks at you
with a glint in his eyes, only describable as manic focus.""",
                      None,
                      1,2],
            '022':["Run away",
                      """YOU WON""",
                      None],
            '0211':["Use the stick to pry open the door",
                       """Begrudgingly you walk over to the door and shove the
stick that you found earlier into the gap. Putting all of your weight behind
the bar, the door gently creaks open. Inside it is completely dark. The sorcerer
points down the dark hallway and hisses \'Let us go down to the Circles of
Dante.""",
                       "stick",
                       1,2],
            '0212':["Try to overpower the sorcerer",
                       """You lunge at the sorcerer but right before you reach
him he vanishes into a cloud of black smoke and reappears in the opposite corner
of the room. He starts hoarsely spouting an incantation and you see a bright light,
then pure darkness. You hear water dripping and it seems you are in a cave.
You starve.
"""]
           }

#'path string':[description as a next choice,
#               description as current,
#               req items,
#               nextpaths (variable incrementing num of paths)
#]
#if its a death path has no req items or nextpaths
#if its a win path it has current desc="YOU WON"
