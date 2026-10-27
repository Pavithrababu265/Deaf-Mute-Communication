try:
    import mediapipe.python.solutions as solutions
    print("Deep import successful")
    print(dir(solutions))
except ImportError as e:
    print(f"Deep import failed: {e}")

try:
    import mediapipe as mp
    print(f"mp.solutions? {hasattr(mp, 'solutions')}")
except Exception as e:
    print(e)
