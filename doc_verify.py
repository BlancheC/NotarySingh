#Author: Blanche Chung
#Created Date: Spring 2023
#Description: This file contains functions to create and verify digital signatures.
# Needs to be intergrated

def hash_buffer(device_buffer, hashed_buffer):import hashlib
import numpy as np
import pyopencl as cl

kernel_code = '''
#pragma OPENCL EXTENSION cl_khr_byte_addressable_store : enable

__kernel void hash_buffer(__global uchar *device_buffer, __global uchar *hashed_buffer)
{
    int idx = get_global_id(0);
    int hashed_buffer_size = get_global_size(0);

    if (idx < hashed_buffer_size)
    {
        char hex[2];
        uint8_t digest[32];
        uchar buffer[1];
        buffer[0] = device_buffer[idx];
        sha256(buffer, 1, digest);

        for (int i = 0; i < 32; i++)
        {
            uchar nibble1 = (digest[i] >> 4) & 0xF;
            uchar nibble2 = digest[i] & 0xF;
            hashed_buffer[idx*64 + i*2] = (nibble1 > 9 ? nibble1 - 10 + 'a' : nibble1 + '0');
            hashed_buffer[idx*64 + i*2 + 1] = (nibble2 > 9 ? nibble2 - 10 + 'a' : nibble2 + '0');
        }
    }
}
'''


def verify_document(document_content, stored_hash):
    # Convert document content to a numpy array
    content_bytes = np.array(list(document_content), dtype=np.uint8)

    # Set up OpenCL context and queue
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    # Create a buffer on the device for the document content
    device_buffer = cl.Buffer(ctx, cl.mem_flags.READ_ONLY, content_bytes.nbytes)
    hashed_buffer = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, content_bytes.nbytes * 64)

    # Copy the content_bytes to the device
    cl.enqueue_copy(queue, device_buffer, content_bytes)

    # Compile the kernel
    prg = cl.Program(ctx, kernel_code).build()

    # Execute the kernel
    global_size = (content_bytes.size, )
    local_size = None
    prg.hash_buffer(queue, global_size, local_size, device_buffer, hashed_buffer)

    # Move the hashed buffer back to the host
    hashed_content = np.empty(content_bytes.nbytes * 64, dtype=np.uint8)
    cl.enqueue_copy(queue, hashed_content, hashed_buffer)

    # Check if the stored hash matches the hash of the provided document content
    return stored_hash == hashed_content.tobytes()

    for i in range(hashed_buffer.size):
        hashed_buffer[i] = hashlib.sha256(device_buffer[i]).hexdigest()

def verify_document(document_content, stored_hash):
    # Convert document content to a bytearray
    content_bytes = bytearray(document_content)

    # Create a buffer on the device for the document content
    with dpctl.device_context("opencl:gpu:0"):
        device_buffer = DeviceArray.from_host_numpy(content_bytes)
        hashed_buffer = DeviceArray(device_buffer.size, dtype=numba.byte)

        # Hash the document content on the device
        hash_buffer(device_buffer, hashed_buffer)

        # Move the hashed buffer back to the host
        hashed_content = hashed_buffer.to_host_numpy()

    # Check if the stored hash matches the hash of the provided document content
    return stored_hash == hashed_content
