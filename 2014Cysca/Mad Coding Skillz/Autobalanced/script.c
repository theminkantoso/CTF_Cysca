#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
	// Constants
#define LENGTH 28
#define RANGE 1170
#define SIZE (RANGE *LENGTH *2 + 1)
#define BUFFER_SIZE 256

static unsigned char Q[SIZE][LENGTH+1];

int answer_length(int l, int *v, int *S, int s, int n, int b, int a)
{
	// no solution found within length
	if (l <= 0)
		return 0;
	// solution found at correct length
	if (v[n] + s == 0 && l == 1)
	{
		S[n] = 1;
		return 1;
	}

	// traverse excluding "me"
	if (Q[s- b][n + 1] && answer_length(l, v, S, s, n + 1, b, a))
		return 1;
	// traverse include "me"
	int temp = s + v[n];
	if (temp >= b && temp <= a && Q[s- b + v[n]][n + 1] && answer_length(l- 1, v, S, s + v[n], n + 1, b, a))
	{
		S[n] = 1;
		return 1;
	}
}

// Populate result matrix
int subsetsum_matrix(int *values, int a, int b)
{
	int s, n;
	int diff = a- b;
	// initialise to false
	for (s = 0; s <= diff; s++)
	{
		for (n = 0; n <= LENGTH; n++)
			Q[s][n] = 0;
	}

	for (n = LENGTH- 1; n >= 0;--n)
	{
		for (s = b; s <= a;++s)
		{
			int self = values[n] + s == 0;
			// excluding "me" is there a solution
			int exclude = Q[s- b][n + 1];
			// including "me" is there a solution
			int include = 0;
			int temp = s + values[n];
			if (temp >= b && temp <= a)
				include = Q[s- b + values[n]][n + 1];
			// save result
			Q[s- b][n] = self || exclude || include;
		}
	}

	return Q[-b][0];
}

// auxiliary line reading function
ssize_t read_line(int fd, char **buf)
{
	ssize_t size = BUFFER_SIZE, length = 0;
	char c;
	*buf = malloc(sizeof(char) *(size + 1));
	while (read(fd, &c, 1) != 0 && c != '\n')
	{
		// save character
		(*buf)[length++] = c;
		// extend buffer if necessary
		if (length == size)
		{
			size += size;
			*buf = realloc(*buf, sizeof(char) *(size + 1));
		}
	}

	// null terminate
	(*buf)[length] = '\0';
	return length;
}

int main(int argc, char *argv[])
{
	int *values = malloc(sizeof(int) *LENGTH);
	int *solution = malloc(sizeof(int) *LENGTH);
	char *buf;
	int i, success;
	// connect to server
	struct addrinfo hints, *res;
	memset(&hints, 0, sizeof(struct addrinfo));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	getaddrinfo("192.168.100.210", "9876", &hints, &res);
	int fd = socket(res->ai_family, res->ai_socktype, res->ai_protocol);
	connect(fd, res->ai_addr, res->ai_addrlen);
	FILE *fp;
	fp = fdopen(fd, "w");
	int num = 0;
	char *tok;
	char *str;
	// read banner (no error handling :O!)
	read_line(fd, &buf);
	printf("%s\n", buf);
	free(buf);
	read_line(fd, &buf);
	printf("%s\n", buf);
	free(buf);
	for (num = 0; num<10; num++)
	{
		// read round number
		read_line(fd, &buf);
		printf("%s\n", buf);
		free(buf);
		// read length
		read_line(fd, &buf);
		printf("%s\n", buf);
		for (str = buf; *str && *str != ':'; str++);
		int length = atoi(++str);
		free(buf);
		// Parse ints in line
		read_line(fd, &buf);
		printf("%s\n", buf);
		for (str = buf; *str && *str != ':'; str++);
		tok = strtok(++str, " ");
		for (i = 0; tok && i<LENGTH; i++)
		{
			values[i] = atoi(tok);
			tok = strtok(NULL, " ");
		}

		free(buf);
		// calculate subset sum
		memset(solution, 0, sizeof(int) *LENGTH);
		int a = 0;	// positive sum
		int b = 0;	// negative sum
		for (i = 0; i<LENGTH; i++)
			if (values[i] > 0)
				a += values[i];
		else
			b += values[i];
		success = subsetsum_matrix(values, a, b) &&
			answer_length(length, values, solution, 0, 0, b, a);
		// print solution
		if (success)
		{
			for (i = 0; i<LENGTH;++i)
				if (solution[i])
				{
					fprintf(fp, "%d ", values[i]);
					printf("%d ", values[i]);
				}

			fprintf(fp, "\n");
			printf("\n");
			fflush(fp);
		}
		else
		{
			fprintf(fp, "no solution\n");
			printf("no solution\n");
			fflush(fp);
		}

		// read "correct"
		read_line(fd, &buf);
		printf("%s\n", buf);
		free(buf);
	}

	// read flag
	read_line(fd, &buf);
	printf("%s\n", buf);
	free(buf);
	// cleanup
	fclose(fp);
	close(fd);
	free(values);
	free(solution);
}