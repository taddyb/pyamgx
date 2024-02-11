cdef extern from "mpi.h":

    ctypedef int MPI_Comm  # Assuming MPI_Comm is an int

    int MPI_Init(int *argc, char ***argv)
    int MPI_Finalize()
