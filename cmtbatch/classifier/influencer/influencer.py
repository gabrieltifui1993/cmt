from client.elastichsearch.constants import Influence


def calculate_user_score(usr_values, max_values):
    """
    :param tweets: last user tweets
    :param max_values: dictionary containing the global max values
    :return:
    """

    score = int(usr_values[Influence.MAX_RETWEETS]) / int(max_values[Influence.MAX_RETWEETS]) \
            + int(usr_values[Influence.MAX_LIKES]) / int(max_values[Influence.MAX_LIKES])     \
            + int(usr_values[Influence.MAX_REPLIES]) / int(max_values[Influence.MAX_REPLIES])

    return score