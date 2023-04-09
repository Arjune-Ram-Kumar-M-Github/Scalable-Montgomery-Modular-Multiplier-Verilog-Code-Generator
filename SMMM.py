class SynthesizeVerilogCode:
    def __init__(self,N,W):
        self.N = N
        self.W = W
        self.E = (N+2)//W + 1

        self.noBits_X_Y_M = self.N*self.E - 1

        self.noBits_N = len(bin(N)[2:])
    

    def writeCode(self):
        f = open("VerilogCode.v","w+")

        f.write("module scalableMMM(input wire [{}:0] X,Y,M,output reg [{}:0][{}:0] Z);\n".format(self.noBits_X_Y_M,self.E-1,self.W-1))

        f.write( "reg [{}:0] N,W,E;\nreg c_a,c_b;\nreg [{}:0] q,tempZ,tempZ2;\nreg [{}:0] temp;\n".format(self.noBits_N,self.W-1,self.W))

        f.write(" integer i,j;\ninitial begin\nZ = 0;\nN = {};\nW = {};\nE = {};\nc_a = 0;\nc_b = 0;\nq = 0;\ntemp =0;\ntempZ = 0;\ntempZ2 = 0;\ni = 0;\nj = 0;\nend\n".format(self.N,self.W,self.E))

        f.write("always@(*) begin\nif(i < N) begin\nc_a = 0;\nc_b = 0;\n".format(self.N))

        for iter in range(0,self.E):
            if iter == 0:
                f.write("j = 0;\ntemp = Z[j] + X[j*W +: {}]*Y[i] + c_a;\nc_a = temp[W];\nZ[j] = temp[0 +: {}];\nq = Z[0];\ntemp = Z[j] + q[0]*M[j*W +: {}] + c_b;\nc_b = temp[W];\nZ[j] = temp[0 +: {}];\n".format(self.W,self.W,self.W,self.W))
            else:
                f.write("j = {};\ntemp = Z[j] + X[j*W +: {}]*Y[i] + c_a;\nc_a = temp[W];\nZ[j] = temp[0 +: {}];\ntemp = Z[j] + q[0]*M[j*W +: {}] + c_b;\nc_b = temp[W];\nZ[j] = temp[0 +: {}];\n".format(iter,self.W,self.W,self.W,self.W))

                f.write("tempZ = Z[j];\ntempZ2 = Z[j-1];\n Z[j-1]= {}tempZ[0],tempZ2[1 +: {} ]{};\n".format("{",self.W-1,"}"))

        f.write("end\nend\nendmodule")

        f.close()

        print("Code Generated")
        
def possibleW(N):
    print("---------------------------------------------------------------------------------------------")
    for w in range(2,N+1):
        if ((N+2)/w).is_integer():
            print("Possible Value of W : {}".format(w))
    print("----------------------------------------------------------------------------------------------")




if __name__ == "__main__":
    N = int(input("Enter the bit size of M : "))
    possibleW(N)
    W = int(input("Enter the processing word bit size : "))
    sv = SynthesizeVerilogCode(N,W)
    sv.writeCode()
