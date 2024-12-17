def normalize(max_grade: float, result: float) -> float:
  if result <=0:
    return 0
  if result > max_grade:
    return max_grade
  
  return result / max_grade * 10