
(*
  creer une fonction recursive "quicksort" qui prend en parametre la liste a trier
  cas terminale: si la liste est vide retourner la liste vide
                si la liste contient un seul element retourner la liste avec ce seule element
  - choisir un pivot (de preference le dernier element de la liste si possible)
  - partitionner la liste en deux sous-listes:
  - les elements inferieurs au pivot
  - les elements superieurs ou egals au pivot
  - appeler la fonction recursive sur les deux premieres sous-listes
  - combiner les deux sous-listes pour obtenir la liste triee

*)





let rec partitionner liste pivot less more = match liste with
  | [] -> [], []
  | t :: reste ->
      if t < pivot then (partitionner reste pivot ([t]::less) more)
      else (partitionner reste pivot less ([t]::more))
;;


let quicksort liste = 
  match liste with
  | [] -> []
  | [a] -> [a]
  | pivot :: reste ->
      let plus_petit, plus_grand = partitionner liste pivot [] [] in
      plus_petit @ [pivot] @ plus_grand
;;


let l = [1;2;8;6];;

quicksort l;;