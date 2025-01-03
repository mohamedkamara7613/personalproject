
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
  |[] -> less, more
  |x :: reste ->
      if x <= pivot then (partitionner reste pivot (x::less) more)
      else (partitionner reste pivot less (x::more))
;;


let rec quicksort liste = match liste with
  |[] -> []
  |pivot :: reste ->
      let less, more = partitionner reste pivot [] [] in
      quicksort less @ [pivot] @ quicksort more
;;



let l = [1;2;8;6];;

quicksort l;;

(*Version Iterative*)