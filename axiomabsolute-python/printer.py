def pr_str(mal):
  # If it's a list, map str over elements, join with spaces and surround parens
  # Otherwise just str it.
  if isinstance(mal, list):
    return'(' + ' '.join([pr_str(x) for x in mal]) + ')'
  elif isinstance(mal, tuple):
    return '[' + ' '.join([pr_str(x) for x in mal]) + ']'
  elif mal == None:
    return 'nil'
  elif mal == True:
    return 'true'
  elif mal == False:
    return 'false'
  else:
    return repr(mal)