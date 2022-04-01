/*---------------------------------------------------------------------------
-- (c) Copyright: OscillatorIMP Digital
-- Author : Ivan Ryger
-- Creation date : 2021/26/11
---------------------------------------------------------------------------*/
// further reading on pointers
// https://dyclassroom.com/c/c-pointers-and-two-dimensional-array
// https://overiq.com/c-programming-101/pointers-and-2-d-arrays/ 

// for debugging purposes on a compiler not having all the necessary OSCIMP libraries
// works only on synthetic data
// #define DEBUG 

#include<stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include<string.h>
#include<math.h>

#ifndef DEBUG
#include <fcntl.h>
#include <unistd.h>  // for sleep()
#include "utils_conf.h"
#include "fir_conf.h"// library for communicating with the FIR
#include "axi_to_dac_conf.h"
#endif

#define FLOAT_T 2
#define INT_T 1
#define SHORT_T 0

// input data format is [x1,y1,x2,y2,...xn,yn]; containing N-readings
// result is pointer to 2x2 array representing the covariance matrix
//in format [<x,x> <x,y>; <x,y> <y,y>]
void cov_interleaved(short int *data_in, int length, float *cov_matrix)
{	
	float x_mean = 0, y_mean = 0;
	float xx = 0, xy = 0, yy = 0;

	int i = 0;
	// find the mean value
	for (i = 0; i < length; i++)
	{
		x_mean = x_mean + *(data_in + i*2);
		y_mean = y_mean + *(data_in + i*2 + 1);
	}
	x_mean = x_mean / length;
	y_mean = y_mean / length;
	
	// printf("\nxmean = %f, ymean =%f, length = %f\n",x_mean, y_mean,(float)length);
	// calculate covariances
	for ( i = 0; i < length; i++)
	{
		xx = xx + (*(data_in + i*2) - x_mean)*(*(data_in + i*2) - x_mean);
		xy = xy + (*(data_in + i*2) - x_mean)*(*(data_in + i*2 + 1) - y_mean);
		yy = yy + (*(data_in + i*2 + 1) - y_mean)*(*(data_in + i*2 + 1) - y_mean);
 	}
	xx = xx / (length-1);
	xy = xy / (length-1);
	yy = yy / (length-1);

	*(cov_matrix) = xx;
	*(cov_matrix + 1) = xy;
	*(cov_matrix + 2) = xy;
	*(cov_matrix + 3) = yy;

}
// computes the eigenvalue diagonalization of matrix a
// A = T*D*T', where 
// T is matrix whose columns are eigenvectors, and
// D is square matrix with respective eigenvalues on the diagional;
void eig_2x2(float *a, float *d, float *t)
{
    float disc, l1, l2,n1,n2;
    float a11, a12, a21, a22;
    a11 = *a;
    a12 = *(a+1);
    a21 = *(a+2);
    a22 = *(a+3);
   //discriminant of eigenvalue characteristic equation (quadratic for 2x2 matrix) 
    disc = (a11+a22)*(a11+a22)-4*(a11*a22-a21*a12);
    //pair of eigenvalues
    l1 = 0.5*((a11+a22) - sqrt(disc));
    l2 = 0.5*((a11+a22) + sqrt(disc));

    *d = l1;
    *(d+1) = 0;
    *(d+2) = 0;
    *(d+3) = l2;

    // normalize the length of eigenvectors
    //norm of the eigenvectors
    n1 = sqrt((a11-l1)*(a11-l1) + a21*a21);
    n2 = sqrt((a11-l2)*(a11-l2) + a21*a21);

    
    //compute the eigenvectors from matrix null space as
    //(A - lambda.I)*e = [0;0], [e1,e2] = null(A-lambda.I)
    //nullspace of A is orthogonal to column space of A-lambda.I
    *t = -a21/n1;
    *(t + 1) = -a21/n2;
    *(t + 2) = (a11-l1)/n1;
    *(t + 3) = (a11-l2)/n2;
}

// matrix 2-norm defined as a maximal sinuglar value of matrix a
float diag_matrix_norm(float *a, int n)
{
    float max = 0;//temporary value to store maximum of the diagonal entries
    for (int i =0; i < n; i++)
    {
        if (fabs(*(a + i*(n + 1))) > max)
            max = fabs(*(a + i*(n + 1)));
      //  printf("\nfabs(a(i,i)) = %f, max = %f", fabs(*(a + i*(n+1))),max);
    }
    return(max);
}
// compute the maxium of matrix entries
float matrix_max_element( float *mat, const int rows, const int cols)
{
    float tmp=0;
    
    for(int k = 0; k < rows; k++) // row iteration
	{
	    for(int l = 0; l < cols; l++) // column iteration
	    {
			if (fabs(*(mat + k*cols + l)) > tmp)
			    tmp = fabs(*(mat + k*cols + l));
	//	printf("new maximum is %f \n",tmp);
		
	    }
	}
return(tmp);
}

// computes inverse square root of diagonal entries of square diagonal matrix A
void diag_matrix_inverse_sqrt(float *a, int n)
{
    for (int i =0; i < n; i++)
    {
      //  printf("entry i = %d. old value %3.3f\n",i,*(a + i*(n + 1)));
        *(a + i*(n + 1)) = 1/sqrt(*(a + i*(n + 1)));
      //  printf("entry i = %d. new value %3.3f\n",i,*(a + i*(n + 1)));
    }
}
// this function currently works only on square matrices
void transpose_nxn(float *mat, int n)
{
    float tmp;
	{
	    for(int i = 0; i < n; i++) // row iteration
	        for (int j = 0; j < i; j++)//column iteration
	        {
	           tmp = *(mat + i*n + j);
	           *(mat + i*n + j)=*(mat + j*n + i);
	           *(mat + j*n + i)= tmp;
	        }
	}
}
// matrix c*E(m,n)*F(n,p) = G(m,p)
// pointer can be also used on 2D array as  int *ptr = &num[0][0];
void scalar_x_mat_x_mat(float c, float *e, int e_row, int e_col, float *f, int f_row, int f_col, float *g)
{
    float tmp;
    for(int i = 0; i < e_row ; i++)// iterate through rows of matrix e
	    for (int j = 0; j < f_col; j++) // iterate through columns of matrix f
	    {
	        tmp = 0;
	        for (int k = 0; k < e_col; k++)// iterate through the inner dimension of product
	        {
	        
	        tmp = tmp + (*(e + i*e_col + k))*(*(f + k*f_col + j)); //e[i][k]*f[k][j];
	        //printf("\n i = %d, j = %d, k = %d, tmp = %2.2f",i,j,k,tmp);
	            
	        }
	        *(g + i*f_col +j) = c*tmp; // g[i][j]
	    }
}



float scale_entries_to_int16(float *mat, const int rows, const int cols, signed short int *mout)
{
    float max = matrix_max_element(mat,rows,cols);
    float scale_factor = 32767/max;
   // printf("scale factor is %f, maximum is %f \n\n",scale_factor,max);
    
    for( int i = 0; i < rows; i++)
        for(int j =0; j < cols; j++)
        {
            *(mout + i*cols + j) = (signed short int)round(scale_factor*(*(mat + i*cols + j)));
        }
    return(scale_factor);
}

// works only with floating point matrices
void print_matrix(FILE *fout, const char *text, void *mat, int type, const int rows, const int cols)
{
    if (fout ==NULL)
        fout = stdout;

    fprintf(fout, "\n%s\n", text);
    switch(type)
    {
        case SHORT_T:
            for(int k = 0; k < rows; k++) // row iteration
	        {
	            for(int l = 0; l < cols; l++) // column iteration
			        fprintf(fout,"%d , ",*(((short int*)mat + k*cols + l)));
		        fprintf(fout,"\n");
	        }
	        break;
	    case INT_T: 
            for(int k = 0; k < rows; k++) // row iteration
	        {
	            for(int l = 0; l < cols; l++) // column iteration
			        fprintf(fout,"%d , ",*(((int*)mat + k*cols + l)));
		        fprintf(fout,"\n");
	        }
	        break;
	    case FLOAT_T:
	        for(int k = 0; k < rows; k++) // row iteration
	        {
	            for(int l = 0; l < cols; l++) // column iteration
		    	    fprintf(fout,"%f , ",*(((float*)mat + k*cols + l)));
		        fprintf(fout,"\n");
	        }
	        break;
    }
}
int main(int argc, char *argv[])
{

    enum print{QUIET,COMPUTATION,DATA,ALL};
	unsigned char print = QUIET, pr =0, save = 0;
	FILE *dumpfile;
	
	FILE *fout = stdout;
	
	for(int ii = 0; ii < argc; ii++)
	{
	    if(strstr(argv[ii], "-dump") != NULL)
		    save = ii;
        
        if((ii == save + 1) && (ii > 1))
    		if ((dumpfile=fopen(argv[ii],"w"))== NULL)
	    	{	
		    	printf("error opening file %s, data will not be saved\n",argv[4]);
			    save = 0;
		    }
        
        if(strstr(argv[ii],"-print")!= NULL)
            pr = ii;
            
        if ((ii == pr + 1)&&(ii > 1))
            {
                if (strstr(argv[ii],"quiet")!= NULL)
                    print = QUIET;
                if (strstr(argv[ii],"computation")!= NULL)
                    print = COMPUTATION;
                if (strstr(argv[ii],"data")!= NULL)
                    print = DATA;
                if (strstr(argv[ii],"all")!= NULL)
                    print = ALL;
            }
            
        
        if(strstr(argv[ii],"-help")!= NULL)
          //  printf("\n%s -print quiet|computation|data|all filename|stdout -dump dumpfile \n",argv[0],)
            printf("\n%s -print quiet|computation|data|all  -dump dumpfile \n",argv[0]);
	}
	
/*
    if (argc > 2)
    {
	
	if(strstr(argv[1], "-print") != NULL)
		if(atoi(argv[2]) == 1)
			print = 1;

	if(strstr(argv[3], "-file") != NULL)
	{
		save = 1;

		if ((fo=fopen(argv[4],"w"))== NULL)
		{	
			printf("error opening file %s, data will not be saved\n",argv[4]);
			save = 0;
		}
	if (save == 1)
	    fclose(fo);	
	}
        
    }
*/
	

#ifndef DEBUG
#define BUFFER_SIZE 16384
    signed short int dataIQ[BUFFER_SIZE * 2];
    int fi;
    fi=open("/dev/dataComplex_to_ram_0",O_RDWR);
    read(fi,dataIQ,BUFFER_SIZE*2*sizeof(signed short int));
    close(fi);
#endif 

#ifdef DEBUG
// test data
#define BUFFER_SIZE 360
short int dataIQ[] = {11612, 11575,
11621, 11815,
11626, 12034,
11614, 12159,
11539, 12340,
11575, 12628,
11471, 12695,
11505, 12928,
11470, 13004,
11462, 13334,
11478, 13531,
11326, 13691,
11384, 13756,
11209, 13906,
11277, 14097,
11237, 14289,
11110, 14296,
11024, 14393,
11001, 14579,
10940, 14718,
10862, 14696,
10791, 14930,
10785, 15091,
10641, 15235,
10572, 15291,
10466, 15371,
10424, 15583,
10356, 15702,
10070, 15500,
10107, 15695,
9996, 15849,
9857, 15857,
9766, 15911,
9725, 16045,
9681, 16264,
9467, 16060,
9310, 16304,
9255, 16392,
9108, 16322,
8909, 16094,
8787, 16221,
8675, 16392,
8595, 16363,
8462, 16437,
8305, 16352,
8194, 16419,
7969, 16327,
7867, 16388,
7698, 16302,
7618, 16330,
7458, 16229,
7249, 16174,
7168, 16268,
7013, 16326,
6839, 16200,
6611, 16123,
6409, 16025,
6320, 16016,
6119, 15916,
5965, 15987,
5787, 15885,
5642, 15776,
5424, 15733,
5355, 15640,
5026, 15535,
4961, 15495,
4606, 15221,
4434, 15128,
4333, 15050,
4196, 15063,
3988, 14820,
3887, 14858,
3431, 14457,
3355, 14495,
3176, 14254,
3039, 14254,
2746, 13937,
2544, 13910,
2411, 13707,
2230, 13606,
1963, 13367,
1838, 13358,
1516, 12994,
1289, 12720,
1226, 12784,
984, 12498,
753, 12407,
515, 12096,
446, 11943,
190, 11719,
-23, 11540,
-274, 11263,
-449, 11199,
-775, 10817,
-837, 10695,
-1013, 10477,
-1205, 10249,
-1450, 10006,
-1693, 9853,
-1868, 9684,
-2045, 9394,
-2217, 9149,
-2487, 8831,
-2744, 8434,
-2726, 8492,
-3195, 7981,
-3324, 7808,
-3424, 7614,
-3609, 7398,
-3832, 7105,
-3997, 6764,
-4239, 6548,
-4333, 6424,
-4418, 6239,
-4866, 5781,
-4952, 5461,
-5062, 5262,
-5300, 5053,
-5497, 4652,
-5656, 4434,
-5731, 4193,
-6004, 3852,
-6174, 3604,
-6339, 3404,
-6654, 2881,
-6707, 2690,
-6883, 2364,
-6923, 2269,
-7221, 1777,
-7382, 1512,
-7517, 1294,
-7776, 941,
-7764, 807,
-8045, 440,
-8128, 90,
-8284, -48,
-8385, -382,
-8550, -661,
-8692, -942,
-8808, -1324,
-8913, -1486,
-9105, -1869,
-9207, -2025,
-9284, -2445,
-9488, -2847,
-9480, -2881,
-9642, -3345,
-9709, -3455,
-9835, -3760,
-10017, -4110,
-9986, -4190,
-10133, -4618,
-10253, -4859,
-10313, -5142,
-10400, -5403,
-10399, -5547,
-10667, -6100,
-10595, -6096,
-10762, -6540,
-10816, -6719,
-10866, -6969,
-10934, -7318,
-11085, -7547,
-11013, -7818,
-11160, -7970,
-11273, -8356,
-11270, -8525,
-11330, -8790,
-11314, -9046,
-11345, -9204,
-11435, -9578,
-11379, -9664,
-11550, -10022,
-11524, -10271,
-11585, -10472,
-11441, -10567,
-11600, -10910,
-11531, -11010,
-11564, -11256,
-11513, -11447,
-11570, -11631,
-11506, -11796,
-11624, -12076,
-11580, -12315,
-11490, -12312,
-11443, -12618,
-11484, -12783,
-11545, -13055,
-11522, -13309,
-11397, -13317,
-11500, -13699,
-11321, -13649,
-11301, -13839,
-11306, -14137,
-11162, -14139,
-11210, -14385,
-11065, -14292,
-11069, -14734,
-11021, -14628,
-10847, -14752,
-10997, -15163,
-10684, -15008,
-10760, -15310,
-10645, -15234,
-10548, -15393,
-10449, -15431,
-10339, -15604,
-10237, -15600,
-10154, -15638,
-10110, -15863,
-9977, -15849,
-9848, -15929,
-9729, -16088,
-9623, -15977,
-9413, -16048,
-9423, -16173,
-9265, -16100,
-9137, -16177,
-9127, -16358,
-8957, -16429,
-8779, -16365,
-8705, -16427,
-8503, -16368,
-8395, -16413,
-8264, -16397,
-8139, -16420,
-8007, -16314,
-7756, -16263,
-7614, -16288,
-7461, -16252,
-7278, -16221,
-7289, -16310,
-6965, -16118,
-6851, -16151,
-6693, -16141,
-6445, -15910,
-6347, -16131,
-6278, -16065,
-6021, -15943,
-5896, -15909,
-5721, -15808,
-5493, -15667,
-5293, -15615,
-5144, -15510,
-5000, -15431,
-4611, -15213,
-4629, -15256,
-4353, -15085,
-4250, -15000,
-4063, -15052,
-3816, -14736,
-3601, -14591,
-3441, -14575,
-3329, -14500,
-3079, -14228,
-2848, -14086,
-2661, -13961,
-2508, -13793,
-2241, -13648,
-2116, -13684,
-1849, -13362,
-1607, -13047,
-1521, -13070,
-1316, -12765,
-923, -12626,
-813, -12327,
-664, -12248,
-383, -12035,
-242, -11814,
-65, -11617,
103, -11406,
345, -11321,
638, -10904,
907, -10740,
965, -10569,
1152, -10392,
1368, -10155,
1506, -9971,
1702, -9816,
1895, -9522,
2081, -9323,
2396, -8982,
2582, -8690,
2817, -8433,
2940, -8284,
3148, -8005,
3393, -7780,
3529, -7520,
3730, -7251,
4004, -7048,
4141, -6711,
4305, -6440,
4503, -6161,
4667, -5925,
4818, -5735,
5009, -5408,
5338, -5024,
5381, -4821,
5613, -4580,
5812, -4271,
5996, -3962,
6105, -3691,
6355, -3406,
6478, -3125,
6557, -2961,
6865, -2447,
6989, -2362,
7101, -2045,
7257, -1862,
7396, -1518,
7603, -1245,
7802, -816,
7853, -728,
8076, -147,
8196, -182,
8291, 299,
8483, 572,
8544, 732,
8691, 1018,
8857, 1427,
8907, 1615,
9091, 1968,
9245, 2241,
9427, 2526,
9421, 2763,
9484, 3084,
9614, 3314,
9743, 3592,
9940, 3889,
10022, 4260,
10123, 4503,
10310, 4869,
10326, 5088,
10374, 5268,
10519, 5573,
10561, 5905,
10543, 5967,
10763, 6389,
10807, 6646,
10900, 6908,
11033, 7282,
11046, 7459,
11171, 7806,
11081, 7825,
11150, 8099,
11264, 8508,
11250, 8609,
11353, 8926,
11510, 9173,
11351, 9353,
11479, 9657,
11404, 9759,
11507, 10088,
11376, 10155,
11487, 10376,
11565, 10631,
11568, 11032,
11581, 11123,
11672, 11519,
11544, 11534};
#endif

#define ROWS 2
#define COLS 2

	if ((print == ALL)||(print == DATA))
		print_matrix(fout, "IQ data",&dataIQ[0],SHORT_T,BUFFER_SIZE,COLS);
	if(save > 0)
	{
	    print_matrix(dumpfile, "IQ data",&dataIQ[0],SHORT_T,BUFFER_SIZE,COLS);
		fclose(dumpfile);
    }
//	float data[2*N] = {1,2,2,4,3,6,4,8,5,10};	
	float C[2][2]; // covariance matrix
	float D[2][2], T[2][2], M[2][2];// diagonal eigenvalue matrix, eigenvector matrix,
                                    // and correction (product) matrix
	cov_interleaved(dataIQ,BUFFER_SIZE,&C[0][0]);
	
	if ((print == COMPUTATION)|| (print == ALL))
		print_matrix(fout, "cov interleaved",&C[0][0],FLOAT_T,ROWS,COLS);
    /*
	float a[4] = {3,-1,-1,3};
	//float d[4], t[4];
	float d[2][2], t[2][2];
	
	//eig_2x2(a,d,t);
	eig_2x2(a,&d[0][0],&t[0][0]);
    */
	eig_2x2(&C[0][0],&D[0][0],&T[0][0]);
    
	if ((print == COMPUTATION)|| (print == ALL))
		print_matrix(fout, "eigenvalue matrix",&D[0][0],FLOAT_T,ROWS,COLS);
		
 /*   
    float norm = 0;
	norm = diag_matrix_norm(&D[0][0],2);
	
	norm = sqrt(norm);
	
	if (print == 1)
		printf( "\neigenvalue matrix D 2-norm =%3.2f\n",norm);
*/	
	diag_matrix_inverse_sqrt(&D[0][0],2);
	
	if ((print == COMPUTATION)|| (print == ALL))
		print_matrix(fout,"inverse square root 1/sqrt(D)",&D[0][0],FLOAT_T,ROWS,COLS);

	if ((print == COMPUTATION)|| (print == ALL))
		print_matrix(fout, "eigenvector matrix T",&T[0][0],FLOAT_T,ROWS,COLS);   
	
	transpose_nxn(&T[0][0],2);

	if ((print == COMPUTATION)|| (print == ALL))
		print_matrix(fout, "matrix transpose T'",&T[0][0],FLOAT_T,ROWS,COLS);
		
//	scalar_x_mat_x_mat(norm, &D[0][0],ROWS,COLS,&T[0][0],ROWS,COLS,&M[0][0]);
    scalar_x_mat_x_mat(1, &D[0][0],ROWS,COLS,&T[0][0],ROWS,COLS,&M[0][0]);
    
	if ((print == COMPUTATION)|| (print == ALL))
		print_matrix(fout, "product matrix M = k *sqrt(diag(D))*T' ",&M[0][0],FLOAT_T,ROWS,COLS);

	signed short int M_integer[2][2]={{0,0},{0,0}};
    
    float scale_factor = 0;
    
	scale_factor = scale_entries_to_int16(&M[0][0],ROWS,COLS,&M_integer[0][0]);
	
	if ((print == COMPUTATION)|| (print == ALL))	
	    printf("\nscale factor is %f\n",scale_factor);

//	M_integer[0][0] = -32767;
//    M_integer[0][1] = 27436;
//    M_integer[1][0] = -5179;
//    M_integer[1][1] = -6185;
	
	if ((print == QUIET)||(print == COMPUTATION)|| (print == ALL))
		print_matrix(fout, "scaled correction matrix M_integer",&M_integer[0][0],SHORT_T,ROWS,COLS);

    printf("\nmatrix computation terminated successfully\n");

/*
mapping of I-Q signals in the tcl script: 
i' = i x m11 + q x m12
q' = i x m21 + q x m22

m11 = matrix_mxi(A), m21 = matrix_mxi(B)
m12 = matrix_myq(A), m22 = matrix_myq(B)
*/    

#ifndef DEBUG
    int retval1 = EXIT_FAILURE, retval2 = EXIT_FAILURE;
    retval1= axi_to_dac_full_conf("/dev/matrix_mxi",M_integer[0][0],M_integer[1][0],BOTH_ALWAYS_HIGH,1);// axi_to_dac /dev/dds_ampl
    retval2= axi_to_dac_full_conf("/dev/matrix_myq",M_integer[0][1],M_integer[1][1],BOTH_ALWAYS_HIGH,1);// axi_to_dac /dev/dds_ampl
    
    if (retval1 == EXIT_SUCCESS)
        fprintf(fout,"matrix_mxi updated successfully\n");
    else
        fprintf(fout,"matrix_mxi failed to update\n");
     if (retval2 == EXIT_SUCCESS)
        fprintf(fout,"matrix_myq updated successfully\n");
    else
        fprintf(fout,"matrix_myq failed to update\n");
/*	this needs to be done also for integers
	scalar_x_mat_x_mat(float c, float *e, int e_row, int e_col, float *f, int f_row, int f_col, float *g)
    print matrix can be adjusted on fly, whether to dump everything to stderr or file
    in loop fprintf( matrix IQ, matrix IQ corrected), fprintf correction factor

   fclose(fo);
*/
#endif
    return(0);
}


