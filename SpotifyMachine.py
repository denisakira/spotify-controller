from pynput import keyboard
import requests
import spotipy
import spotipy.util as util

"""
App que escuta pelas teclas F6, F7, F8 e F9 no teclado para dar
play ou pause no spotify.

Referências:

Key listener: https://stackoverflow.com/a/43106497/9944198
"""

token = None


def play():
    r = requests.put('https://api.spotify.com/v1/me/player/play',
                     params={
                         "access_token": token,
                         "token_type": "Bearer",
                     })
    print(r.text)
    return r


def pause():
    r = requests.put('https://api.spotify.com/v1/me/player/pause',
                     params={
                         "access_token": token,
                         "token_type": "Bearer",
                     })
    print(r.text)    
    return r


def next_song():
    r = requests.post('https://api.spotify.com/v1/me/player/next',
                      params={
                          "access_token": token,
                          "token_type": "Bearer",
                      })
    print(r.text)    
    return r


def previous_song():
    r = requests.post('https://api.spotify.com/v1/me/player/previous',
                      params={
                          "access_token": token,
                          "token_type": "Bearer",
                      })
    print(r.text)    
    return r


def auth():
    global token
    username = 'Denis Akira'
    scope = 'user-modify-playback-state'
    res = util.prompt_for_user_token(username, scope)
    token = res


stateChoices = {
    'f6': previous_song,
    'f7': play,
    'f8': pause,
    'f9': next_song,
}


def stateMachine(arguments):
    state = stateChoices.get(arguments)
    return state()


def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys

    if k in ['f6', 'f7', 'f8', 'f9']:  # keys interested
        r = stateMachine(k)
        if r.status_code == 401:
            auth()


if __name__ == "__main__":
    lis = keyboard.Listener(on_press=on_press)
    lis.start()  # start to listen on a separate thread
    lis.join()
