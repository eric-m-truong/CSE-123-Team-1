#include<iostream>
#include<vector>
#include <limits>
using namespace std;

int main (void){
    int count=0;
    //take inputs as floats
    float number = 0, average=0;
    vector<float> arr;
    while(1){
        cin>>number;
        if(cin.fail()){
            cout<<"Wrong input"<<endl;
            cin.clear();
            cin.ignore(numeric_limits<std::streamsize>::max(), '\n');
        }
        else{
            if (count>=20) {
                // print out values and get average of array
                for(auto item: arr){
                    // print out array
                    //cout << item << " ";
                    average = average + item;
                }
                cout << endl;
                // print total sum of array
                //cout<< "Total: " << average <<endl;
                average = average/20;
                cout<< "Average is "<< average << endl;
                count=0;
                arr.clear();
            }
            
            //insert to array
            arr.insert(arr.end(), number);
            count++;
            //cout<<"count: "<< count<< " is " << number<<endl;
        }
    }
    return 0;
}
