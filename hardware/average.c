/**
 Take inputs from stdin and average every 20 data points. The inputs (ints or floats) can be entered 
 in 1 line seperated by whitespaces and/or on seperate lines. Any invalid inputs
 (non-numeric or newlines) will be ignored and not used in the running average. 
 */
 
 /**
 Notes:
    atof() also works for integers and returns 0.0 if there is no valid conversion, but an input of 0 will also return 0.0.
    Have to loop through each character of the input because of this.
 */
 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define DATA_BUFFER 4096
#define DATA_COUNT 20

int main(void){
    // flag: keeps track of decimal points when scanning tokens
    // count: track number of inputs
    // valid: low if input is numeric
    int flag = 0,count=0, valid=0;
    
    // average: keep running total, do average calc once count==20
    // buff: char array to hold getline input
    // data: pointer to input array (buff)
    float average = 0;
    char buff[DATA_BUFFER];
    char *data;
    data = buff;
    size_t data_buffer = DATA_BUFFER;
    
    // s: delimeter for tokenization
    const char s[2] = " ";
    
    /*Get line by line from stdin, buffer limited to size of DATA_BUFFER
      anything larger than DATA_BUFFER will break the code*/
    while(getline(&data, &data_buffer, stdin)){
        //printf("Line is: %s\n", data);
        // tokenize line with delimeter," "
        char *token;
        token = strtok(data, s);
        while( token != NULL ) {
          //printf( "Token: %s\n", token );
          if (!(strcmp(token, "\n")) || !(strcmp(token, "\r\n"))){
              //skip any \n or \r\n
              valid=1;
          }
          else{
              for (int i=0;i<strlen(token); i++){
                //loop through token and verify if numeric/float (ignore newlines and carridge returns)
                if ((isdigit(token[i])!=0) || (token[i]=='.') || (token[i]=='\r') || (token[i]=='\n')){
                   if (token[i]=='.') flag++;
                   if (flag>1) {
                        // more than one decimal point, do not include in calculations
                        valid=1;
                        break;
                    }
                }
                else{
                    // char is not valid
                    valid=1;
                    break;
                }
              }
          }
          if (valid==0){
              // valid input, do calculations
              float float_convert = atof(token);
              average+=float_convert;
              count++;
              printf("Count %d\t Token: %f\n", count, float_convert);
              if (count>=DATA_COUNT){
                // do average and reset average,count
                printf("Get average of %f: %f\n", average, average/20);
                average = 0;
                count=0;
              }
          }
          //else printf("Invalid input: %s\n", token);  // debug statement to check invalid inputs
          valid=0;
          flag=0;
          token = strtok(NULL, s);
       }
    }
    return 0;
}

/*example inputs:
1 2 3 4 5 6 7 8 9 1 2 3 4 5 6 7 8 9 1 2
10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10 10
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20

should give:
4.65
10
10.5
---> can also put inputs on seperate lines
*/
