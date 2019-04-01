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
                     """sit02""",
                     None,
                     1,2],
               '03':["Go up mountain"
                     ,"""sit03"""
                     None,
                     1,2],
               '021':["stick",
                      """sit021""",
                      None,
                      1,2,3],
               '022':[None,
                      """sit022""",
                      None,
                      1,2]}

itemchoices
