# RX-compiler
New compiler to display and learn about basic compilers creation through the use of Python with Yacc and Lex


## Manual de usuario en español:

RX es un lenguaje enfocado a operaciones matemáticas sencillas, existen los diferentes tipos de objetos y se declaran de las siguientes formas:
Estructura general:
La estructura general del código de un programa se ve como el siguiente ejemplo

<code>
program programName; 

//Lines of comments to be ignored by the compiler

//Global Variables

vars

    int num1, num2, num3;
    float flt1, num4, flt2; // <-- the name for variables must start with a character, 
    char textXYZ;           // followed by more characters or numbers  

//Global functions

func int fibonacci(int fiboNum){
    
    //Local variables to the function
    
    vars 
        int fibRes1, fibRes2, fibResR;
    
    // If-else loop
    if (fiboNum <= 1){
        return fiboNum; //Return statute
    }
       
    else{

        fibRes1 = fibonacci(fiboNum - 1);
        fibRes2 = fibonacci(fiboNum - 2);
        fibResR = fibRes1 + fibRes2;
        return fibResR;
    }
       
}

//Main body of the program
main()
{
    // Local variables
    vars
        int local1, local2, result;
        float A, B, C, D;

    //Assigning values to variables
    numero1 = 10;
    numero2 = 20;
    result = 0;

    // While loop
    while(A > B * C){
       A = A-D;
       print(A);
    }

    // For loop 
    for indexF = 15 to 25 by 2 do{
        result = result + 1;
        print(indexF,  "_nl");
    }
        
    //Print statute using a new line "_nl" append at the end for line break 
    print("Resultado: ", resultado, "_nl");



</code >
<br>
## Variables:
Primero se declara el estatuto “vars”, seguido de alguno de los tipos disponibles
<ul>
<li>	Entero: int num1;</li>
<li>	Flotante: float num2;</li>
<li>	Booleano: bool boolVar;</li>
<li>	Caracter: char “texto”;</li>
</ul>
Quedando la estructura de la siguiente forma:
<code>
vars <br>
    int A, B, C;<br>
    float D, E, F, G, H, I, J;<br>
    char = charX, charY;<br>
    bool X, Y, Z;
</code>
<br>
<br>
Es importante terminar cada estatuto con un punto y coma ‘;’ y separar con comas las variables que se declaran del mismo tipo como se ve en el anterior ejemplo.
<br>
Las variables pueden ser de tipo global o local, dependiendo de si se declaran al inicio del programa (variables globales) antes que las funciones y que el main() o si se declaran dentro de alguna función o el cuerpo de main() (locales). Una variable global puede ser accesada y modificada en cualquier parte del programa por cualquier función o por main(). Las variables locales solamente pueden ser accesadas en el scope de la función o main() donde se declaran. Al ser variables locales, se pueden declarar varias variables con el mismo nombre en diferentes funciones o main(). Si se intenta declarar una variable local con el mismo nombre que una global o una global con el mismo nombre que otra global, el programa arrojará un error de que se está intentando repetir el nombre de la variable.
<br>

## Arreglos: 
A la vez se pueden generar arreglos o matrices de alguno de los tipos anteriormente descritos generándolos de la siguiente forma:
int Arreglo[tamaño];
int Matriz[tamaño] [tamaño];
Quedando la estructura de la siguiente forma para declarar un arreglo de 10 casillas y una matríz de 2 filas x 5 columnas (teniendo un total de 10 casillas):
<br>
<code>
vars 
    int Array1[10];
    float Matrix1[2][5];
</code>

Los arreglos y matrices tienen el mismo tipo de propiedades que las variables con la diferencia de que son capaces de almacenar más de 1 valor. El tamaño de los arreglos y las matrices tiene que ser especificado al inicio en su declaración seguido del nombre del arreglo o matríz y estando dentro de brackets “[ ]”. 
<br>

## For loops:
Los for loops pueden tener las siguientes formas:
<code>
for indexVariable = 1 to 11 do{
    ...
}
</code>
<br>
En este ejemplo, se crea la variable “indexVariable” si no existía antes y se le asigna el valor de uno. Si ya existía previamente en otro scope entonces simplemente se le asigna ese valor. Como no se especificó el estatuto “by X” avanzará de 1 en 1 hasta llegar a 10, un número antes que 11 establecido en el segundo estatuto. La secuencia sería 1, 2, 3, 4, 5, 6, 7, 8, 9, 10.
<br>
<code>
for indexVariable = 15 to 25 by 2 do{
    ...
}
</code>
<br>
En este otro caso avanzaría del 15 al 23 de dos en dos, dando la siguiente secuencia: 15, 17, 19, 21, 23.
<br>
El for loop también soporta operaciones dentro de sus parámetros y números flotantes tales como el siguiente ejemplo:<br>
<code>
   for K = 1 to -2 * -2.5 by 1.5 do{
       B = C - D;
   }
</code>
<br>

## While loops:
Los while loops tienen la siguiente forma:
<br>
<code>
   while(A > B * C){
       A = A-D;
       print(A);
   }
</code>
<br><br>
Este ciclo se ejecuta siempre y cuando la condición se cumpla. Dentro del ciclo debe de haber algo que altere la variable de control y haga cambiar el resultado para no caer en un loop infinito. 
<br><br>

## If & if-else:
Los estatutos if-simple o if-else tienen la siguiente forma:
If simple:
<br><code>
if (X <= 1){
        //Comments
        Do something…
    }

If-else:
if (X <= 1){
        //Comments
        Do something…
    }
       
    else{
       //Comment number 2, if first condition not met, then
        Do something else…
    }
</code>

Un ejemplo práctico de un estatuto If-else sería el siguiente:
<br><code>
    if (fiboNum <= 1){
        //print(fiboNum);
        return fiboNum;
    }
       
    else{
       //print(fiboNum);

        fibRes1 = fibonacci(fiboNum - 1);
        fibRes2 = fibonacci(fiboNum - 2);
        fibResR = fibRes1 + fibRes2;
        return fibResR;
    }
</code>
Lo que esté dentro de un cuerpo if solamente será ejecutado si se cumple la condición que se está queriendo evaluar. En caso de ser un if-else, lo que está dentro del cuerpo else será automáticamente ejecutado si la primera condición del if no se cumple, pero será ignorado si la condición inicial sí se cumple.
<br><br>

## Funciones
Las funciones se declaran al inicio del código después de las variables globales, se pueden declarar 1 o más funciones y tienen la siguiente estructura:
<br><code>
//Global function of return type int
func int nameOfFunction(int parameter1, int parameter2){ 

    //Local variables to the function
    vars 
        int fibRes1, fibRes2, fibResR;
    
    // If-else loop
   Some code actions here 
	...
   return result; //Return statute of the same type as the declared func type.
    
}
</code>
<br>
<br>
La función regresa el tipo de parámetro que se declara al inicio y puede ser de tipo “int”, “float”, “char” o “bool”.
<br><br>

## Recursividad
El lenguaje RX permite recursividad (funciones que se llaman a sí mismas) y es similar a otros lenguajes de programación, basta con invocar la llamada a la función dentro de la misma función. Es necesario poner un caso límite en el cual la función deje de llamarse a sí misma.
Ejemplo de recursividad con una función de Fibonacci:

<code>

//Global functions

func int fibonacci(int fiboNum){

    //Local variables to the function

    vars 
        int fibRes1, fibRes2, fibResR;
    
    // If-else loop
    
    if (fiboNum <= 1){
        return fiboNum; //Return statute
    }
       
    else{

        fibRes1 = fibonacci(fiboNum - 1);
        fibRes2 = fibonacci(fiboNum - 2);
        fibResR = fibRes1 + fibRes2;
        return fibResR;
    }
       
}
</code>
