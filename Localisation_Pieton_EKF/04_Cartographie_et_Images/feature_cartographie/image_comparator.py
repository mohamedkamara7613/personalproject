import cv2
import os

class ImageComparator:
    """
    Classe permettant de comparer deux images en utilisant l'algorithme ORB (Oriented FAST and Rotated BRIEF).
    """
    
    def __init__(self, nfeatures=2000, min_match_count=30, max_width=800, distance_threshold=50):
        self.nfeatures = nfeatures
        self.min_match_count = min_match_count
        self.max_width = max_width
        self.distance_threshold = distance_threshold
        self.orb = cv2.ORB_create(nfeatures=self.nfeatures)
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    def _load_and_preprocess(self, image_input):
        if isinstance(image_input, str):
            if not os.path.exists(image_input):
                raise FileNotFoundError(f"L'image '{image_input}' est introuvable.")
            img = cv2.imread(image_input, cv2.IMREAD_GRAYSCALE)
            if img is None:
                raise ValueError(f"Impossible de lire l'image : {image_input}")
        else:
            if len(image_input.shape) == 3:
                img = cv2.cvtColor(image_input, cv2.COLOR_BGR2GRAY)
            else:
                img = image_input
                
        h, w = img.shape
        if w > self.max_width:
            ratio = self.max_width / w
            img = cv2.resize(img, (self.max_width, int(h * ratio)))
            
        return img

    def compare(self, ref_image_input, test_image_input, debug=False):
        """
        Compare deux images. Retourne un dict avec 'match', 'score', 'error'
        """
        img1 = self._load_and_preprocess(ref_image_input)
        img2 = self._load_and_preprocess(test_image_input)

        kp1, des1 = self.orb.detectAndCompute(img1, None)
        kp2, des2 = self.orb.detectAndCompute(img2, None)

        if des1 is None or des2 is None:
            return {"match": False, "score": 0, "error": "Pas assez de points caractéristiques"}

        matches = self.bf.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        good_matches = [m for m in matches if m.distance < self.distance_threshold]
        
        match_count = len(good_matches)
        is_match = match_count >= self.min_match_count

        if debug:
            img_matches = cv2.drawMatches(
                img1, kp1, img2, kp2, good_matches[:50], None, 
                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
                matchColor=(0, 255, 0)
            )
            cv2.imshow(f"ORB Debug - Match: {is_match} ({match_count})", img_matches)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return {
            "match": is_match,
            "score": match_count,
            "error": None
        }
