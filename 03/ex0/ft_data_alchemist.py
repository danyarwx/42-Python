#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   ft_data_alchemist.py                                 :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: dzhukov <dzhukov@student.42heilbronn.de>     +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/26 18:01:30 by dzhukov             #+#    #+#            #
#   Updated: 2026/04/26 18:21:44 by dzhukov            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

import sys

def ft_command_quest() -> None:
	print("=== Command Quest ===")
	print(f"Program name: {sys.argv[0]}")
	total = len(sys.argv)
	received = total - 1
	if received == 0:
		print("No arguments provided!")
	else:
		print(f"Arguments received: {received}")
		for i in range(1, total):
			print(f"Argument {i}: {sys.argv[i]}")
	print(f"Total arguments: {total}")


if __name__ == "__main__":
	ft_command_quest()
