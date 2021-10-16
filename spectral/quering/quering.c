#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LINE_MAX_LEN 512

int main()
{
    char const *path_original = "~M stellar class, ref30 (3588).txt";
    char const *path_reduced = "~M stellar class, ref30 (3588) (reduced).txt";

    FILE *original = fopen(path_original, "r");
    FILE *reduced = fopen(path_reduced, "w");

    size_t n = 0;
    size_t N = 100;
    size_t start_Mag = 0;
    double Mag;

    char line[LINE_MAX_LEN];
    char buffer[LINE_MAX_LEN];
    int scan_error;

    size_t line_n = 0;
    while (fgets(line, LINE_MAX_LEN, original) != NULL)
    {   ++line_n;
        if (strstr(line, "Mag R") != NULL)
        {   start_Mag = strstr(line, "Mag R") - line;
            break;
        }
    }
    fgets(line, LINE_MAX_LEN, original);
    ++line_n;

    while (fgets(line, LINE_MAX_LEN, original) != NULL)
    {   ++line_n;
        memcpy(buffer, line + start_Mag, 6);
        buffer[6] = 0;
        scan_error = sscanf(buffer, "%lf", &Mag);
        if (scan_error == 1)
            if (Mag <= 4)
            {   memcpy(buffer, strchr(line, '|') + 1, strchr(strchr(line, '|') + 1, '|') - strchr(line, '|') - 1);
                buffer[strchr(strchr(line, '|') + 1, '|') - strchr(line, '|') - 1] = 0;
                fprintf(reduced, "%s\n", buffer);
                if (++n == N)
                    break;
            }
    }

    fclose(original);
    fclose(reduced);
}
