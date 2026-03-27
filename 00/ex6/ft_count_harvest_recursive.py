#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_count_harvest_recursive.py                        :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/03/27 16:50:08 by dzhukov             #+#    #+#            #
#   Updated: 2026/03/27 16:53:24 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

def recursion(days: int):
    if days > 1:
        recursion(days - 1)
    print("Day", days)


def ft_count_harvest_recursive():
    days = int(input("Days until harvest: "))
    recursion(days)
    print("Harvest time!")
