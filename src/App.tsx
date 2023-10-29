// Global import 
import axios from "axios";
import * as z from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { useState } from "react";
import {
    FieldValues,
    SubmitHandler,
    useForm
} from 'react-hook-form';


//components
import { Input } from "./components/ui/input";
import { Button } from './components/ui/button'
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from './components/ui/form';


const inputschema = z.object({
    srcurl: z.string().url().optional(),
});

function App() {

    const [isLoading, setIsLoading] = useState(false);


    const form = useForm<z.infer<typeof inputschema>>({
        resolver: zodResolver(inputschema),
        defaultValues: {
            srcurl: ""
        },
    })

    const onSubmit = async (data: z.infer<typeof inputschema>) => {
        setIsLoading(true);
        console.log(data);

       const response =  await axios.post('/prediction', data)
            .catch(() => {
                console.log("Error")
            })
            .finally(() => {
                setIsLoading(false);
            })
        // setIsLoading(false);
    }

    return (
        <>
            <Form {...form} >
                <form className="" onSubmit={form.handleSubmit(onSubmit)}>
                    <div className="max-w-screen-lg mx-auto">
                        <div className="grid grid-cols-1 md:grid-cols-8 md:gap-10 mt-6">

                            <div className="col-span-4 flex flex-col gap-3 pr-18">

                                {/*  Div for Avatar and Constant Details */}
                                <div className="flex flex-row gap-x-20">
                                    <FormField
                                        control={form.control}
                                        name="srcurl"
                                        render={({ field, formState }) => (
                                            <FormItem className="w-full">
                                                <FormLabel className="flex gap-2 items-center">Enter a url Here *</FormLabel>
                                                <FormControl>
                                                    {/* Spread onBlur , onChange , value , name , ref by using ...field , and thus we handle all those fields*/}
                                                    <Input required {...field} disabled={isLoading} />
                                                </FormControl>
                                                <FormMessage />
                                            </FormItem>
                                        )}
                                    />

                                    <span className="flex flex-row gap-3 mb-5">
                                        <Button className="w-2/3 rounded px-5 py-2.5 overflow-hidden group bg-green-500 relative hover:bg-gradient-to-r hover:from-green-500 hover:to-green-400 text-white transition-all ease-out duration-300"
                                            type="submit" disabled={isLoading} >
                                            <span className="absolute right-0 w-8 h-32 -mt-12 transition-all duration-1000 transform translate-x-12 bg-white opacity-10 rotate-12 group-hover:-translate-x-40 ease"></span>
                                            Submit
                                        </Button>
                                    </span>

                                </div>
                            </div>

                            {/*  End of Profile Section */}
                        </div>
                    </div>
                </form>
            </Form>
        </ >
    );
}

export default App;